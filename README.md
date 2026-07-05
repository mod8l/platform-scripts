# platform-scripts

Reusable deployment helpers, cost-optimization scripts, observability snippets, and advisory tools for ML platforms and the startups that run them.

I built these scripts to make repetitive platform work faster and safer: cleaning up stale resources before they become expensive, right-sizing requests before an AWS bill becomes a board topic, and assessing whether a team is ready to scale before they commit to a major platform investment.

**Related work:** [`ml-inference-starter`](../ml-inference-starter) for a reference serving stack, [`ml-security-checklist`](../ml-security-checklist) for security and production readiness, and [`engineering-playbook`](../engineering-playbook) for the R&D processes these scripts support.

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
| Deployment | [`deployment/terraform/aws-gpu-node-pool/`](deployment/terraform/aws-gpu-node-pool/) | EKS GPU (NVIDIA) managed node group |
| Deployment | [`deployment/terraform/azure-gpu-node-pool/`](deployment/terraform/azure-gpu-node-pool/) | AKS GPU (NVIDIA NC-series) node pool |
| Cost Optimization | [`cost-optimization/aws/idle-ebs-volumes.py`](cost-optimization/aws/idle-ebs-volumes.py) | Find unattached EBS volumes |
| Cost Optimization | [`cost-optimization/gcp/unused-disks.sh`](cost-optimization/gcp/unused-disks.sh) | Find unattached GCP disks |
| Cost Optimization | [`cost-optimization/k8s/rightsize-requests.py`](cost-optimization/k8s/rightsize-requests.py) | Suggest K8s request adjustments |
| Cost Optimization | [`cost-optimization/cloud-cost-baseline.py`](cost-optimization/cloud-cost-baseline.py) | Baseline spend summary from AWS or GCP billing CSV |
| Observability | [`observability/promql/`](observability/promql/) | PromQL query snippets |
| Observability | [`observability/grafana-dashboards/gpu-cluster.json`](observability/grafana-dashboards/gpu-cluster.json) | GPU cluster Grafana dashboard |
| Observability | [`observability/alerts/prometheus-rules.yml`](observability/alerts/prometheus-rules.yml) | Prometheus alerting rules |
| CLI | [`cli/repo_health/`](cli/repo_health/) | Repository health checker |
| Advisory | [`advisory/ml-maturity-assessment.py`](advisory/ml-maturity-assessment.py) | ML platform maturity assessment |
| Advisory | [`advisory/technical-due-diligence-checklist.md`](advisory/technical-due-diligence-checklist.md) | Technical due diligence checklist |

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
