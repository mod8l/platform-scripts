# Terraform module: AKS node pool with NVIDIA GPUs.
# This module assumes the target AKS cluster already exists.

terraform {
  required_version = ">= 1.3.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.0.0"
    }
  }
}

data "azurerm_kubernetes_cluster" "cluster" {
  name                = var.cluster_name
  resource_group_name = var.resource_group_name
}

resource "azurerm_kubernetes_cluster_node_pool" "gpu" {
  name                  = var.node_pool_name
  kubernetes_cluster_id = data.azurerm_kubernetes_cluster.cluster.id
  vm_size               = var.vm_size
  node_count            = var.node_count
  os_type               = "Linux"
  mode                  = "User"

  min_count = var.min_count
  max_count = var.max_count

  node_labels = var.node_labels
  node_taints = [for t in var.node_taints : "${t.key}=${t.value}:${t.effect}"]

  tags = var.tags

  lifecycle {
    ignore_changes = [node_count]
  }
}
