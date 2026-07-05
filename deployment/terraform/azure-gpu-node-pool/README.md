# AKS GPU Node Pool (NVIDIA NC-series)

Terraform module to add a GPU-enabled user node pool to an existing Azure AKS cluster.

## Requirements

- Terraform >= 1.3.0
- AzureRM provider >= 3.0.0
- Existing AKS cluster
- Subscription quota for NC-series VMs in the target region

## Usage

```hcl
module "aks_gpu_pool" {
  source              = "./deployment/terraform/azure-gpu-node-pool"
  resource_group_name = "my-rg"
  cluster_name        = "my-cluster"
  vm_size             = "Standard_NC6s_v3"
  node_count          = 1
  min_count           = 0
  max_count           = 3
}
```

## Variables

See [`variables.tf`](variables.tf) for all configurable options.

## Notes

- Node pool name must be alphanumeric and lowercase, 1-12 characters.
- Nodes are tainted by default so that only GPU workloads schedule on them.
- `min_count` defaults to 0 to allow scale-to-zero cost optimization.
- Install the NVIDIA device plugin and GPU drivers via the AKS GPU node pool add-on
  or DaemonSet before scheduling workloads.
