variable "cluster_name" {
  description = "Name of the existing EKS cluster"
  type        = string
}

variable "node_group_name" {
  description = "Name of the GPU managed node group"
  type        = string
  default     = "gpu-node-group"
}

variable "node_role_arn" {
  description = "IAM role ARN for EKS worker nodes"
  type        = string
}

variable "subnet_ids" {
  description = "Subnet IDs where GPU nodes will be launched"
  type        = list(string)
}

variable "instance_type" {
  description = "GPU instance type for nodes"
  type        = string
  default     = "g4dn.xlarge"
}

variable "capacity_type" {
  description = "ON_DEMAND or SPOT capacity for GPU nodes"
  type        = string
  default     = "ON_DEMAND"
}

variable "disk_size" {
  description = "Root volume size in GB"
  type        = number
  default     = 100
}

variable "desired_size" {
  description = "Desired number of GPU nodes"
  type        = number
  default     = 1
}

variable "min_size" {
  description = "Minimum number of GPU nodes"
  type        = number
  default     = 0
}

variable "max_size" {
  description = "Maximum number of GPU nodes"
  type        = number
  default     = 3
}

variable "max_unavailable_percentage" {
  description = "Maximum percentage of nodes unavailable during updates"
  type        = number
  default     = 25
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
      key    = "nvidia.com/gpu"
      value  = "true"
      effect = "NO_SCHEDULE"
    }
  ]
}
