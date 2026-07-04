#!/usr/bin/env python3
"""
Purpose: Analyze Kubernetes container resource requests and suggest right-sizing.
Inputs:
  --kubeconfig   Path to kubeconfig (default: KUBECONFIG env or ~/.kube/config)
  --namespace    Namespace to analyze (default: all namespaces)
  --factor       Buffer factor over measured usage (default: 1.2)
Outputs: Suggested CPU/memory requests per container.
Risks: Recommendations are heuristic; validate in non-production before applying.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys


def run_kubectl(args: list[str]) -> tuple[str, str, int]:
    kubectl = shutil.which("kubectl") or "kubectl"
    cmd = [kubectl] + args
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return result.stdout, result.stderr, result.returncode


def get_pods(namespace: str | None) -> list[dict]:
    args = ["get", "pods", "-o", "json"]
    if namespace:
        args += ["-n", namespace]
    else:
        args.append("--all-namespaces")
    stdout, stderr, rc = run_kubectl(args)
    if rc != 0:
        print(f"Failed to list pods: {stderr}", file=sys.stderr)
        return []
    data = json.loads(stdout)
    return data.get("items", [])


def suggest_request(
    current: str, usage: str | None, resource: str, factor: float
) -> str:
    if usage:
        return f"usage={usage}; consider request near {usage} * {factor}"
    if resource == "cpu":
        return (
            "metrics unavailable; consider starting request at 100m or half the limit"
        )
    return "metrics unavailable; consider starting request at 128Mi or half the limit"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Suggest Kubernetes resource request adjustments."
    )
    parser.add_argument(
        "--kubeconfig",
        default=os.environ.get("KUBECONFIG", os.path.expanduser("~/.kube/config")),
        help="Path to kubeconfig file",
    )
    parser.add_argument("--namespace", help="Namespace to analyze")
    parser.add_argument(
        "--factor",
        type=float,
        default=1.2,
        help="Buffer factor over measured usage",
    )
    args = parser.parse_args()

    os.environ["KUBECONFIG"] = args.kubeconfig

    top_args = ["top", "pod", "--containers"]
    if args.namespace:
        top_args += ["-n", args.namespace]
    else:
        top_args.append("--all-namespaces")

    top_stdout, top_stderr, top_rc = run_kubectl(top_args)
    usages: dict[tuple[str, str, str], tuple[str, str]] = {}
    if top_rc == 0:
        for line in top_stdout.strip().splitlines()[1:]:
            parts = line.split()
            if len(parts) < 5:
                continue
            ns, pod, container, cpu, mem = (
                parts[0],
                parts[1],
                parts[2],
                parts[3],
                parts[4],
            )
            usages[(ns, pod, container)] = (cpu, mem)
    else:
        print(
            f"WARNING: metrics API unavailable ({top_stderr.strip()}); using heuristic fallback.",
            file=sys.stderr,
        )

    pods = get_pods(args.namespace)
    if not pods:
        print("No pods found.")
        return 0

    for pod in pods:
        ns = pod["metadata"].get("namespace", "default")
        pod_name = pod["metadata"].get("name", "unknown")
        spec = pod.get("spec", {})
        for container in spec.get("containers", []):
            cname = container["name"]
            resources = container.get("resources", {})
            requests = resources.get("requests", {})
            cpu_req = requests.get("cpu")
            mem_req = requests.get("memory")
            cpu_usage, mem_usage = usages.get((ns, pod_name, cname), (None, None))

            if cpu_req or mem_req:
                print(f"{ns}/{pod_name}/{cname}")
                if cpu_req:
                    suggestion = suggest_request(cpu_req, cpu_usage, "cpu", args.factor)
                    print(f"  cpu request={cpu_req} -> {suggestion}")
                if mem_req:
                    suggestion = suggest_request(
                        mem_req, mem_usage, "memory", args.factor
                    )
                    print(f"  memory request={mem_req} -> {suggestion}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
