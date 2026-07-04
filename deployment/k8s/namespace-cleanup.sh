#!/usr/bin/env bash
# Purpose: List or delete stale Kubernetes resources (completed/failed pods and jobs)
#          in a namespace. Dry-run by default; pass --dry-run false to delete.
# Inputs:
#   --namespace <ns>      Target namespace (required)
#   --dry-run true|false  Default: true
#   --age-hours <hours>   Minimum age to be considered stale (default: 168)
# Outputs: List of stale resources; deletion commands when dry-run=false
# Risks: Deletes workload data when --dry-run false. Always review the dry-run output first.
set -euo pipefail

NAMESPACE=""
DRY_RUN="true"
AGE_HOURS=168

usage() {
    cat <<EOF
Usage: $(basename "$0") --namespace <namespace> [--dry-run true|false] [--age-hours <hours>]
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --namespace)
            NAMESPACE="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN="$2"
            shift 2
            ;;
        --age-hours)
            AGE_HOURS="$2"
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

if [[ -z "${NAMESPACE}" ]]; then
    echo "ERROR: --namespace is required" >&2
    usage >&2
    exit 1
fi

AGE_SECONDS=$((AGE_HOURS * 3600))
NOW_EPOCH=$(date +%s)

echo "Scanning namespace '${NAMESPACE}' for resources older than ${AGE_HOURS}h (dry-run=${DRY_RUN})"

echo "--- Pods ---"
kubectl get pods -n "${NAMESPACE}" \
    -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.phase}{"\t"}{.metadata.creationTimestamp}{"\n"}{end}' 2>/dev/null \
    | while IFS=$'\t' read -r name phase created; do
        [[ -n "$name" ]] || continue
        case "$phase" in
            Succeeded|Failed|Unknown)
                created_epoch=$(date -u -d "${created}" +%s 2>/dev/null || echo 0)
                if (( NOW_EPOCH - created_epoch >= AGE_SECONDS )); then
                    if [[ "${DRY_RUN}" == "false" ]]; then
                        echo "Deleting pod/${name} (phase=${phase}, age>=${AGE_HOURS}h)"
                        kubectl delete pod "${name}" -n "${NAMESPACE}"
                    else
                        echo "Would delete pod/${name} (phase=${phase}, age>=${AGE_HOURS}h)"
                    fi
                fi
                ;;
            *)
                continue
                ;;
        esac
    done

echo "--- Jobs ---"
kubectl get jobs -n "${NAMESPACE}" \
    -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.conditions[?(@.type=="Complete")].status}{"\t"}{.status.conditions[?(@.type=="Failed")].status}{"\t"}{.metadata.creationTimestamp}{"\n"}{end}' 2>/dev/null \
    | while IFS=$'\t' read -r name complete failed created; do
        [[ -n "$name" ]] || continue
        if [[ "$complete" == "True" || "$failed" == "True" ]]; then
            created_epoch=$(date -u -d "${created}" +%s 2>/dev/null || echo 0)
            if (( NOW_EPOCH - created_epoch >= AGE_SECONDS )); then
                if [[ "${DRY_RUN}" == "false" ]]; then
                    echo "Deleting job/${name} (complete=${complete}, failed=${failed}, age>=${AGE_HOURS}h)"
                    kubectl delete job "${name}" -n "${NAMESPACE}"
                else
                    echo "Would delete job/${name} (complete=${complete}, failed=${failed}, age>=${AGE_HOURS}h)"
                fi
            fi
        fi
    done

echo "Done. Use --dry-run false only after reviewing the list above."
