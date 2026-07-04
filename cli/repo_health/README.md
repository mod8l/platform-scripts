# repo_health

A small CLI that checks a Git repository for essential open-source files.

## Checks

- Git repository (`.git/`)
- README (`README.md` or `README`)
- `LICENSE`
- `.gitignore`
- CI workflow (`.github/workflows/`, `.gitlab-ci.yml`, `.circleci/config.yml`, etc.)

## Usage

```bash
repo-health
repo-health /path/to/repo
```

## Development

```bash
pip install -e '.[dev]'
pytest
```
