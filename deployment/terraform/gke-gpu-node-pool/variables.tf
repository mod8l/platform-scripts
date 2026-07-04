variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region for the node pool"
  type        = string
  default     = "us-central1"
}

variable "cluster_name" {
  description = "Name of the existing GKE cluster"
  type        = string
}

variable "node_pool_name" {
  description = "Name of the GPU node pool"
  type        = string
  default     = "gpu-t4-pool"
}

variable "machine_type" {
  description = "Machine type for GPU nodes"
  type        = string
  default     = "n1-standard-4"
}

variable "min_count" {
  description = "Minimum number of nodes"
  type        = number
  default     = 0
}

variable "max_count" {
  description = "Maximum number of nodes"
  type        = number
  default     = 3
}

variable "accelerator_count" {
  description = "Number of NVIDIA T4 GPUs per node"
  type        = number
  default     = 1
}

variable "node_labels" {
  description = "Labels to apply to nodes"
  type        = map(string)
  default = {
    workload = "gpu"
  }
}

variable "node_taints" {
  description = "Taints to apply to GPU nodes"
  type = list(object({
    key    = string
    value  = string
    effect = string
  }))
  default = [
    {
      key    = "nvidia.com/gpu"
      value  = "true"
      effect = "NO_SCHEDULE"
    }
  ]
}
