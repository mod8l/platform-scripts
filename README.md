# platform-scripts

Reusable deployment helpers, cost-optimization scripts, and observability snippets for ML platforms.

![Lint & Test](https://github.com/gadsosa/platform-scripts/actions/workflows/lint-and-test.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

> **Maturity:** Incubating. These scripts are reference implementations that have been used in real environments. Review and adapt them to your own infrastructure before production use.

## Index

| Category | Script | Purpose |
|---|---|---|
| Deployment | [`deployment/k8s/namespace-cleanup.sh`](deployment/k8s/namespace-cleanup.sh) | List/delete stale namespace resources |
| Deployment | [`deployment/k8s/rolling-restart.sh`](deployment/k8s/rolling-restart.sh) | Safe rolling restart of a Deployment |
| Deployment | [`deployment/k8s/resource-quotas-template.yml`](deployment/k8s/resource-quotas-template.yml) | Namespace resource quota template |
| Deployment | [`deployment/terraform/gke-gpu-node-pool/`](deployment/terraform/gke-gpu-node-pool/) | GKE GPU (NVIDIA T4) node pool |
| Cost Optimization | [`cost-optimization/aws/idle-ebs-volumes.py`](cost-optimization/aws/idle-ebs-volumes.py) | Find unattached EBS volumes |
| Cost Optimization | [`cost-optimization/gcp/unused-disks.sh`](cost-optimization/gcp/unused-disks.sh) | Find unattached GCP disks |
| Cost Optimization | [`cost-optimization/k8s/rightsize-requests.py`](cost-optimization/k8s/rightsize-requests.py) | Suggest K8s request adjustments |
| Observability | [`observability/promql/`](observability/promql/) | PromQL query snippets |
| Observability | [`observability/grafana-dashboards/gpu-cluster.json`](observability/grafana-dashboards/gpu-cluster.json) | GPU cluster Grafana dashboard |
| Observability | [`observability/alerts/prometheus-rules.yml`](observability/alerts/prometheus-rules.yml) | Prometheus alerting rules |
| CLI | [`cli/repo_health/`](cli/repo_health/) | Repository health checker |

## Quickstart

```bash
# Install dev dependencies and the repo_health CLI
make install

# Lint all shell and Python files
make lint

# Run CLI tests
make test

# Format Python code
make format
```

## Safety

- All destructive scripts default to dry-run mode.
- No secrets are hardcoded; scripts rely on environment or tool credentials.
- Review dry-run output before disabling dry-run.

## Contributing

Pull requests are welcome. Please run `make lint` and `make test` before submitting.
