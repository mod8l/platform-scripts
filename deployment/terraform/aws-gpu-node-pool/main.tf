# Terraform module: EKS managed node group with NVIDIA GPUs.
# This module assumes the target EKS cluster already exists.

terraform {
  required_version = ">= 1.3.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0.0"
    }
  }
}

data "aws_eks_cluster" "cluster" {
  name = var.cluster_name
}

resource "aws_eks_node_group" "gpu" {
  cluster_name    = data.aws_eks_cluster.cluster.name
  node_group_name = var.node_group_name
  node_role_arn   = var.node_role_arn
  subnet_ids      = var.subnet_ids

  instance_types = [var.instance_type]
  capacity_type  = var.capacity_type
  ami_type       = "AL2_x86_64_GPU"
  disk_size      = var.disk_size

  scaling_config {
    desired_size = var.desired_size
    min_size     = var.min_size
    max_size     = var.max_size
  }

  update_config {
    max_unavailable_percentage = var.max_unavailable_percentage
  }

  labels = var.node_labels

  dynamic "taint" {
    for_each = var.node_taints
    content {
      key    = taint.value.key
      value  = taint.value.value
      effect = taint.value.effect
    }
  }

  lifecycle {
    ignore_changes = [scaling_config[0].desired_size]
  }
}
