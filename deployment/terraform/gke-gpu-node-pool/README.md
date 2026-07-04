# GKE GPU Node Pool (NVIDIA T4)

Terraform module to add a GPU-enabled GKE node pool to an existing cluster.

## Requirements

- Terraform >= 1.3.0
- GCP project with the GKE API enabled
- Existing GKE cluster

## Usage

```hcl
module "gpu_t4_pool" {
  source       = "./deployment/terraform/gke-gpu-node-pool"
  project_id   = "my-project"
  region       = "us-central1"
  cluster_name = "my-cluster"
}
```

## Variables

See [`variables.tf`](variables.tf) for all configurable options.

## Notes

- Nodes are tainted by default so that only GPU workloads schedule on them.
- `min_count` defaults to 0 to allow scale-to-zero cost optimization.
- GPU driver installation is configured automatically with the latest driver.
