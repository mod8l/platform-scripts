#!/usr/bin/env bash
# Purpose: List unattached GCP persistent disks. Dry-run by default; pass --delete to remove.
# Inputs:
#   --project <project>   GCP project (default: gcloud default)
#   --delete              Actually delete unattached disks
# Outputs: List of disk names and zones; deletion status when --delete is used.
# Risks: --delete destroys data. Create snapshots before deleting.
set -euo pipefail

PROJECT=""
DRY_RUN="true"

usage() {
    cat <<EOF
Usage: $(basename "$0") [--project <project>] [--delete]
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --project)
            PROJECT="$2"
            shift 2
            ;;
        --delete)
            DRY_RUN="false"
            shift
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

GCLOUD_ARGS=()
if [[ -n "${PROJECT}" ]]; then
    GCLOUD_ARGS+=(--project="${PROJECT}")
fi

echo "Finding unattached disks in project '${PROJECT:-default}' (dry-run=${DRY_RUN})..."

mapfile -t disks < <(gcloud compute disks list "${GCLOUD_ARGS[@]}" \
    --filter="NOT users:*" \
    --format="value(name,zone)" \
    2>/dev/null)

if [[ ${#disks[@]} -eq 0 ]]; then
    echo "No unattached disks found."
    exit 0
fi

echo "Found ${#disks[@]} unattached disk(s):"
for line in "${disks[@]}"; do
    read -r name zone <<< "$line"
    echo "  ${name} (zone=${zone})"
    if [[ "${DRY_RUN}" == "false" ]]; then
        echo "  Deleting ${name}..."
        gcloud compute disks delete "${name}" --zone="${zone}" "${GCLOUD_ARGS[@]}" --quiet
    fi
done

echo "Done."
