#!/usr/bin/env bash
# Purpose: Trigger a safe rolling restart of a Kubernetes Deployment and wait for completion.
# Inputs:
#   --namespace <ns>      Namespace containing the deployment (required)
#   --deployment <name>   Deployment name (required)
#   --timeout <seconds>   Rollout status timeout (default: 300)
# Outputs: kubectl rollout commands and status messages
# Risks: Brief availability impact during pod churn; verify cluster capacity first.
set -euo pipefail

NAMESPACE=""
DEPLOYMENT=""
TIMEOUT=300

usage() {
    cat <<EOF
Usage: $(basename "$0") --namespace <ns> --deployment <name> [--timeout <seconds>]
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --namespace)
            NAMESPACE="$2"
            shift 2
            ;;
        --deployment)
            DEPLOYMENT="$2"
            shift 2
            ;;
        --timeout)
            TIMEOUT="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown argument: $1" >&2
            usage >&2
            exit 1
            ;;
    esac
done

if [[ -z "${NAMESPACE}" || -z "${DEPLOYMENT}" ]]; then
    echo "ERROR: --namespace and --deployment are required" >&2
    usage >&2
    exit 1
fi

if ! kubectl get deployment "${DEPLOYMENT}" -n "${NAMESPACE}" >/dev/null 2>&1; then
    echo "ERROR: deployment/${DEPLOYMENT} not found in namespace ${NAMESPACE}" >&2
    exit 1
fi

echo "Restarting deployment/${DEPLOYMENT} in namespace ${NAMESPACE}..."
kubectl -n "${NAMESPACE}" rollout restart deployment/"${DEPLOYMENT}"
kubectl -n "${NAMESPACE}" rollout status deployment/"${DEPLOYMENT}" --timeout="${TIMEOUT}s"
echo "Rollout complete."
