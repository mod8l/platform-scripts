# Technical Due Diligence Checklist — ML Startup

Companion checklist for evaluating the technical health of an ML startup before a funding round,
partnership, or production readiness review.

## How to use this checklist

- For each item, mark `[y]` yes, `[n]` no, or `[?]` needs review.
- Collect evidence (file links, screenshots, runbook references) under **Notes**.
- Aim to have every critical item answered before moving to production scale.

---

## 1. Code

- [ ] Source control is in use (Git) and all production code is tracked.
- [ ] README, LICENSE, and `.gitignore` are present and up to date.
- [ ] Coding standards and a code-review process are documented.
- [ ] Automated tests exist (unit, integration, or smoke) and run in CI.
- [ ] CI/CD pipeline deploys to staging automatically and to production with approval.
- [ ] Dependency versions are pinned (requirements, lock files, Docker image digests).
- [ ] Secrets are not hardcoded; they are injected via environment or a secrets manager.
- [ ] Branch protection and signed commits are enabled for the main branch.
- [ ] Architecture decision records (ADRs) or equivalent design docs are maintained.

## 2. Data

- [ ] Data sources, schemas, and ownership are documented.
- [ ] Data is versioned or backed by immutable snapshots where appropriate.
- [ ] PII / sensitive data is identified and protected (encryption at rest and in transit).
- [ ] Data quality checks run automatically in the pipeline.
- [ ] Training/validation/test splits are reproducible and documented.
- [ ] Data retention and deletion policies comply with relevant regulations.
- [ ] Backups and disaster-recovery plans exist for critical datasets.

## 3. Model

- [ ] Model training code is reproducible (seeded, containerized, dependency-locked).
- [ ] Experiments, hyperparameters, and metrics are tracked (MLflow, Weights & Biases, etc.).
- [ ] Model artifacts are versioned and stored in a model registry.
- [ ] Model evaluation includes fairness, robustness, and error-analysis slices.
- [ ] Model serving latency, throughput, and resource requirements are characterized.
- [ ] Rollback plan exists for model deployments.
- [ ] Model drift and data drift are monitored in production.

## 4. Team

- [ ] Clear engineering org structure and ownership domains are defined.
- [ ] On-call rotation and escalation paths are documented.
- [ ] Team has production ML/Platform/DevOps experience.
- [ ] Documentation and runbooks cover incident response and common failures.
- [ ] Knowledge-sharing practices exist (tech talks, design reviews, retrospectives).
- [ ] Hiring plan addresses gaps in platform, security, and data engineering.

## 5. Security

- [ ] Security policy and responsible-disclosure process are documented.
- [ ] Cloud accounts use multi-factor authentication and least-privilege IAM.
- [ ] Secrets are stored in a dedicated vault (e.g., AWS Secrets Manager, Vault, Azure Key Vault).
- [ ] Dependency and container-image scanning are part of CI.
- [ ] Network segmentation (VPCs, private subnets, firewalls) is in place.
- [ ] Logging and audit trails capture administrative and sensitive actions.
- [ ] Disaster recovery and business continuity plans are tested periodically.

## 6. Operations

- [ ] Production environment is managed as infrastructure as code (Terraform, Pulumi, etc.).
- [ ] Observability stack covers metrics, logs, traces, and alerting.
- [ ] SLIs/SLOs are defined and dashboards are shared with stakeholders.
- [ ] Cost allocation tags and budgets are configured.
- [ ] Autoscaling and resource quotas are tuned for workloads.
- [ ] Change management process includes rollbacks and post-deployment verification.
- [ ] Regular game days or chaos-engineering exercises validate incident response.

---

## Notes

| Area | Evidence / Comments |
|---|---|
| Code | |
| Data | |
| Model | |
| Team | |
| Security | |
| Ops | |
