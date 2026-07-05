# Advisory Tools

Scripts and checklists for technical advisory, ML maturity assessment, and startup due diligence.

## Index

| Tool | Purpose |
|---|---|
| [`ml-maturity-assessment.py`](ml-maturity-assessment.py) | Score an org or repo across CI/CD, observability, security, cost discipline, and data/model lineage |
| [`technical-due-diligence-checklist.md`](technical-due-diligence-checklist.md) | Markdown checklist for ML startup technical due diligence |

## Usage

```bash
# Interactive maturity assessment for the current directory
python advisory/ml-maturity-assessment.py --repo-path .

# Non-interactive assessment with explicit scores
python advisory/ml-maturity-assessment.py \
  --repo-path ./my-project \
  --ci-cd 4 --observability 3 --security 3 --cost 2 --lineage 2 \
  --output advisory/reports/my-project-maturity.md

# Preview report without writing to disk
python advisory/ml-maturity-assessment.py --repo-path . --dry-run
```

## Reports

Generated maturity reports are written to [`reports/`](reports/) by default. Keep client-specific
reports out of version control; only `.gitkeep` is committed to preserve the folder structure.

## Safety

- All reports are generated from read-only inspection.
- `--dry-run` prints the report to stdout instead of writing a file.
- No secrets are requested or stored by these tools.
