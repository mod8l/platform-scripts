variable "resource_group_name" {
  description = "Azure resource group containing the AKS cluster"
  type        = string
}

variable "cluster_name" {
  description = "Name of the existing AKS cluster"
  type        = string
}

variable "node_pool_name" {
  description = "Name of the GPU node pool"
  type        = string
  default     = "gpunp"
}

variable "vm_size" {
  description = "GPU VM size for nodes"
  type        = string
  default     = "Standard_NC6s_v3"
}

variable "node_count" {
  description = "Initial node count for the GPU pool"
  type        = number
  default     = 1
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

variable "node_labels" {
  description = "Labels to apply to GPU nodes"
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
      key    = "sku"
      value  = "gpu"
      effect = "NoSchedule"
    }
  ]
}

variable "tags" {
  description = "Tags to apply to the node pool"
  type        = map(string)
  default     = {}
}
