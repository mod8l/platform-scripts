#!/usr/bin/env python3
"""
Purpose: Build a baseline spend summary from an AWS or GCP billing CSV export.
Inputs:
  --input          Path to a billing CSV file
  --provider       Cloud provider: auto, aws, or gcp (default: auto)
  --output         Optional path for a CSV summary
  --dry-run        Compute and print the summary without writing a file
  --generate-sample Write a sample billing CSV to the given path and exit
Outputs: Spend totals by service and project (stdout and optional CSV).
Risks: Read-only by default; no cloud credentials are used.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

AWS_COLUMNS = {
    "service": [
        "ProductName",
        "product/ProductName",
    ],
    "project": [
        "resourceTags/user:Project",
        "resourceTags/UserProject",
        "lineItem/UsageAccountId",
    ],
    "cost": [
        "lineItem/BlendedCost",
        "lineItem/UnblendedCost",
    ],
}

GCP_COLUMNS = {
    "service": [
        "Description",
        "SKU description",
    ],
    "project": [
        "Project ID",
        "ProjectID",
    ],
    "cost": [
        "Cost",
    ],
}


def pick_column(headers: list[str], candidates: list[str]) -> str | None:
    """Return the first candidate header that exists in the CSV."""
    for candidate in candidates:
        if candidate in headers:
            return candidate
    return None


def detect_provider(headers: list[str]) -> str:
    if pick_column(headers, AWS_COLUMNS["service"]) and pick_column(
        headers, AWS_COLUMNS["cost"]
    ):
        return "aws"
    if pick_column(headers, GCP_COLUMNS["service"]) and pick_column(
        headers, GCP_COLUMNS["cost"]
    ):
        return "gcp"
    raise ValueError(
        "Unable to detect provider. Expected AWS CUR or GCP billing export headers."
    )


def normalize_cost(value: str) -> Decimal:
    """Parse a cost value that may contain a currency symbol or commas."""
    cleaned = value.strip().replace(",", "").replace("$", "").replace("€", "")
    if cleaned in ("", "-"):
        return Decimal("0")
    try:
        return Decimal(cleaned)
    except InvalidOperation as exc:
        raise ValueError(f"Cannot parse cost value: {value!r}") from exc


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        headers = list(reader.fieldnames or [])
        rows = list(reader)
    return headers, rows


def summarize(
    rows: list[dict[str, str]], provider: str
) -> dict[tuple[str, str], Decimal]:
    """Aggregate costs by (service, project)."""
    if provider == "aws":
        service_candidates = AWS_COLUMNS["service"]
        project_candidates = AWS_COLUMNS["project"]
        cost_candidates = AWS_COLUMNS["cost"]
    else:
        service_candidates = GCP_COLUMNS["service"]
        project_candidates = GCP_COLUMNS["project"]
        cost_candidates = GCP_COLUMNS["cost"]

    service_col = (
        pick_column(list(rows[0].keys()), service_candidates) if rows else None
    )
    project_col = (
        pick_column(list(rows[0].keys()), project_candidates) if rows else None
    )
    cost_col = pick_column(list(rows[0].keys()), cost_candidates) if rows else None

    if not rows:
        return {}
    if service_col is None or project_col is None or cost_col is None:
        raise ValueError(
            f"Missing expected columns for provider {provider}. "
            f"Need service/project/cost columns."
        )

    totals: dict[tuple[str, str], Decimal] = defaultdict(Decimal)
    for row in rows:
        service = row.get(service_col, "Unknown").strip() or "Unknown"
        project = row.get(project_col, "Unknown").strip() or "Unknown"
        try:
            cost = normalize_cost(row.get(cost_col, "0"))
        except ValueError:
            continue
        totals[(service, project)] += cost
    return totals


def render_markdown(totals: dict[tuple[str, str], Decimal], provider: str) -> str:
    lines = [
        f"# Cloud Cost Baseline ({provider.upper()})",
        "",
        "| Service | Project | Spend |",
        "|---|---|---:|",
    ]
    total = Decimal("0")
    for (service, project), cost in sorted(
        totals.items(), key=lambda kv: kv[1], reverse=True
    ):
        lines.append(f"| {service} | {project} | ${cost:,.2f} |")
        total += cost
    lines.extend(
        [
            "",
            f"**Total:** ${total:,.2f}",
            "",
            "## Summary by service",
            "",
            "| Service | Spend |",
            "|---|---:|",
        ]
    )
    by_service: dict[str, Decimal] = defaultdict(Decimal)
    by_project: dict[str, Decimal] = defaultdict(Decimal)
    for (service, project), cost in totals.items():
        by_service[service] += cost
        by_project[project] += cost
    for service, cost in sorted(by_service.items(), key=lambda kv: kv[1], reverse=True):
        lines.append(f"| {service} | ${cost:,.2f} |")

    lines.extend(
        [
            "",
            "## Summary by project",
            "",
            "| Project | Spend |",
            "|---|---:|",
        ]
    )
    for project, cost in sorted(by_project.items(), key=lambda kv: kv[1], reverse=True):
        lines.append(f"| {project} | ${cost:,.2f} |")

    return "\n".join(lines)


def write_csv_summary(path: Path, totals: dict[tuple[str, str], Decimal]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["service", "project", "spend"])
        for (service, project), cost in sorted(
            totals.items(), key=lambda kv: kv[1], reverse=True
        ):
            writer.writerow([service, project, f"{cost:.2f}"])


def write_sample_csv(path: Path, provider: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        if provider == "aws":
            writer.writerow(
                [
                    "ProductName",
                    "resourceTags/user:Project",
                    "lineItem/BlendedCost",
                ]
            )
            writer.writerow(["Amazon SageMaker", "model-training", "1200.50"])
            writer.writerow(["Amazon S3", "data-lake", "340.20"])
            writer.writerow(["Amazon EC2", "inference-api", "980.00"])
            writer.writerow(["Amazon CloudWatch", "inference-api", "45.30"])
        else:
            writer.writerow(
                [
                    "Description",
                    "Project ID",
                    "Cost",
                ]
            )
            writer.writerow(["Compute Engine", "ml-platform-prod", "2100.75"])
            writer.writerow(["Cloud Storage", "ml-platform-prod", "410.10"])
            writer.writerow(["Vertex AI", "ml-platform-prod", "850.00"])
            writer.writerow(["Cloud Monitoring", "shared-services", "120.25"])


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a baseline spend summary from a cloud billing CSV."
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="Path to the billing CSV export",
    )
    parser.add_argument(
        "--provider",
        choices=["auto", "aws", "gcp"],
        default="auto",
        help="Cloud provider (default: auto-detect)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Path for the CSV summary output",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the summary without writing any files",
    )
    parser.add_argument(
        "--generate-sample",
        type=Path,
        metavar="PATH",
        help="Generate a sample billing CSV at PATH and exit",
    )
    return parser


def main() -> int:
    parser = build_argument_parser()
    args = parser.parse_args()

    if args.generate_sample:
        provider = args.provider if args.provider != "auto" else "aws"
        write_sample_csv(args.generate_sample, provider)
        print(
            f"Sample {provider.upper()} billing CSV written to: {args.generate_sample}"
        )
        return 0

    if not args.input:
        print(
            "ERROR: --input is required unless --generate-sample is used",
            file=sys.stderr,
        )
        return 1

    input_path = args.input.expanduser().resolve()
    if not input_path.is_file():
        print(f"ERROR: input file not found: {input_path}", file=sys.stderr)
        return 1

    headers, rows = read_csv_rows(input_path)
    provider = args.provider
    if provider == "auto":
        try:
            provider = detect_provider(headers)
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1

    try:
        totals = summarize(rows, provider)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    report = render_markdown(totals, provider)
    print(report)

    if args.dry_run:
        print("\nDry run: no output file written.")
        return 0

    if args.output:
        write_csv_summary(args.output, totals)
        print(f"\nCSV summary written to: {args.output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
