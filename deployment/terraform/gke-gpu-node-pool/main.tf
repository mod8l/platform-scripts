# Terraform module: GKE node pool with NVIDIA T4 GPUs.
# This module assumes the target GKE cluster already exists.

terraform {
  required_version = ">= 1.3.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0.0"
    }
  }
}

data "google_container_cluster" "cluster" {
  name     = var.cluster_name
  location = var.region
  project  = var.project_id
}

resource "google_container_node_pool" "gpu_t4_pool" {
  name     = var.node_pool_name
  location = var.region
  cluster  = data.google_container_cluster.cluster.name
  project  = var.project_id

  autoscaling {
    min_node_count = var.min_count
    max_node_count = var.max_count
  }

  management {
    auto_repair  = true
    auto_upgrade = true
  }

  node_config {
    machine_type = var.machine_type
    image_type   = "COS_CONTAINERD"
    disk_size_gb = 100
    disk_type    = "pd-standard"
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]

    guest_accelerator {
      type  = "nvidia-tesla-t4"
      count = var.accelerator_count
      gpu_driver_installation_config {
        gpu_driver_version = "LATEST"
      }
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

    metadata = {
      disable-legacy-endpoints = "true"
    }
  }
}
