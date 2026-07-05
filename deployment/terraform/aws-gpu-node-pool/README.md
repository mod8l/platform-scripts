# EKS GPU Node Pool (NVIDIA)

Terraform module to add a GPU-enabled managed node group to an existing Amazon EKS cluster.

## Requirements

- Terraform >= 1.3.0
- AWS provider >= 4.0.0
- Existing EKS cluster
- IAM role ARN with the AmazonEKSWorkerNodePolicy, AmazonEKS_CNI_Policy, and
  AmazonEC2ContainerRegistryReadOnly policies attached

## Usage

```hcl
module "eks_gpu_nodes" {
  source          = "./deployment/terraform/aws-gpu-node-pool"
  cluster_name    = "my-cluster"
  node_role_arn   = "arn:aws:iam::123456789012:role/eks-worker-node-role"
  subnet_ids      = ["subnet-abc123", "subnet-def456"]
  instance_type   = "g4dn.xlarge"
  desired_size    = 1
  min_size        = 0
  max_size        = 3
}
```

## Variables

See [`variables.tf`](variables.tf) for all configurable options.

## Notes

- Nodes use the EKS-optimized Amazon Linux 2 GPU AMI (`AL2_x86_64_GPU`).
- Nodes are tainted by default so that only GPU workloads schedule on them.
- `min_size` defaults to 0 to allow scale-to-zero cost optimization.
- The NVIDIA device plugin and DCGM exporter must be installed separately.
