#!/usr/bin/env python3
"""
Purpose: Score an organization or repository across ML platform maturity dimensions.
Inputs:
  --repo-path      Path to the repository or project directory (default: current dir)
  --output         Markdown report path (default: advisory/reports/YYYY-MM-DD-<name>.md)
  --dry-run        Print the report to stdout instead of writing a file
  --ci-cd          Score for CI/CD (1-5)
  --observability  Score for observability (1-5)
  --security       Score for security (1-5)
  --cost           Score for cost discipline (1-5)
  --lineage        Score for data/model lineage (1-5)
Outputs: Markdown maturity report.
Risks: Read-only by default; use --dry-run to preview before writing files.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

DIMENSIONS = {
    "ci_cd": {
        "label": "CI/CD",
        "prompt": "CI/CD: automated builds, tests, and deployments (1-5)",
    },
    "observability": {
        "label": "Observability",
        "prompt": "Observability: metrics, logs, alerts, SLOs (1-5)",
    },
    "security": {
        "label": "Security",
        "prompt": "Security: secrets, IAM, scanning, SBOMs (1-5)",
    },
    "cost": {
        "label": "Cost discipline",
        "prompt": "Cost discipline: budgets, tagging, right-sizing (1-5)",
    },
    "lineage": {
        "label": "Data/model lineage",
        "prompt": "Data/model lineage: versioning, reproducibility, metadata (1-5)",
    },
}


def parse_score(value: str | None) -> int | None:
    """Return an integer score between 1 and 5, or None."""
    if value is None:
        return None
    try:
        score = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"score must be an integer: {value}") from exc
    if score < 1 or score > 5:
        raise argparse.ArgumentTypeError("score must be between 1 and 5")
    return score


def maturity_label(average: float) -> str:
    if average >= 4.0:
        return "Optimizing"
    if average >= 3.0:
        return "Defined"
    if average >= 2.0:
        return "Developing"
    return "Initial"


def collect_scores(args: argparse.Namespace) -> dict[str, int]:
    """Gather scores from CLI flags or interactive prompts."""
    scores: dict[str, int] = {}
    for key in DIMENSIONS:
        value = getattr(args, key)
        if value is None:
            value = prompt_score(DIMENSIONS[key]["prompt"])
        scores[key] = value
    return scores


def prompt_score(prompt: str) -> int:
    """Prompt the user until a valid 1-5 score is entered."""
    while True:
        try:
            raw = input(f"{prompt}: ")
        except (EOFError, KeyboardInterrupt):
            print("\nAborted.", file=sys.stderr)
            raise SystemExit(1) from None
        try:
            return parse_score(raw.strip())  # type: ignore[arg-type]
        except argparse.ArgumentTypeError as exc:
            print(f"Invalid input: {exc}", file=sys.stderr)


def generate_report(repo_path: Path, scores: dict[str, int]) -> str:
    """Render the maturity assessment as Markdown."""
    labels = {key: DIMENSIONS[key]["label"] for key in DIMENSIONS}
    average = sum(scores.values()) / len(scores)
    level = maturity_label(average)

    gaps = [labels[key] for key, score in scores.items() if score <= 2]
    strengths = [labels[key] for key, score in scores.items() if score >= 4]

    lines = [
        "# ML Platform Maturity Assessment",
        "",
        f"- **Repository / project:** `{repo_path}`",
        f"- **Date:** {date.today().isoformat()}",
        f"- **Overall score:** {average:.1f} / 5",
        f"- **Maturity level:** {level}",
        "",
        "## Dimension scores",
        "",
        "| Dimension | Score | Bar |",
        "|---|---|---|",
    ]
    for key in DIMENSIONS:
        score = scores[key]
        bar = "█" * score + "░" * (5 - score)
        lines.append(f"| {labels[key]} | {score}/5 | {bar} |")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            f"The organization is operating at the **{level}** maturity level. "
            f"Average dimension score is **{average:.1f}** out of 5.",
            "",
        ]
    )

    if strengths:
        lines.extend(
            [
                "### Strengths",
                "",
                "- " + "\n- ".join(strengths),
                "",
            ]
        )
    if gaps:
        lines.extend(
            [
                "### Priority gaps",
                "",
                "- " + "\n- ".join(gaps),
                "",
            ]
        )

    lines.extend(
        [
            "## Recommended next steps",
            "",
            "1. Address any dimension scored 2 or lower first.",
            "2. Add objective evidence (CI dashboards, SLO definitions, cost reports) for each score.",
            "3. Re-run this assessment monthly and track trends.",
            "",
        ]
    )

    return "\n".join(lines)


def default_report_path(repo_path: Path) -> Path:
    """Build a default report path inside advisory/reports/."""
    base = repo_path.resolve().name or "project"
    return (
        Path(__file__).resolve().parent
        / "reports"
        / f"{date.today().isoformat()}-{base}-ml-maturity-assessment.md"
    )


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Assess ML platform maturity across key dimensions."
    )
    parser.add_argument(
        "--repo-path",
        default=".",
        help="Path to the repository or project directory",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Markdown report output path",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the report to stdout instead of writing a file",
    )
    for key in DIMENSIONS:
        parser.add_argument(
            f"--{key.replace('_', '-')}",
            type=parse_score,
            default=None,
            help=f"{DIMENSIONS[key]['label']} score (1-5)",
        )
    return parser


def main() -> int:
    parser = build_argument_parser()
    args = parser.parse_args()

    repo_path = Path(args.repo_path).expanduser().resolve()
    if not repo_path.is_dir():
        print(f"ERROR: {repo_path} is not a directory", file=sys.stderr)
        return 1

    scores = collect_scores(args)
    report = generate_report(repo_path, scores)

    if args.dry_run:
        print(report)
        return 0

    output_path = (
        Path(args.output).expanduser().resolve()
        if args.output
        else default_report_path(repo_path)
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Report written to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
