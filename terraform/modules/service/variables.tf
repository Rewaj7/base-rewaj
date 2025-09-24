
#-------------------------#
# Common Variables        #
#-------------------------#
variable "env" {
  description = "Environment (dev/staging/prod)"
}
variable "service_name" {
  description = "Prefix for the ECS service name"
}

#-------------------------#
# ECS Variables           #
#-------------------------#
variable "cluster_arn" {
  description = "The ARN for the parent ECS Cluster resource"
}
variable "desired_count" {
  description = "The desired count of ECS tasks"
}
variable "environment_vars" {
  description = "A map of environment variables names to environment variable values"
}
variable "ssm_secrets" {
  description = "A map of environment variable name to corresponding SSM secret location"
}
variable "template_file_path" {
  description = "Path to the task definition for this service"
}
variable "template_inputs" {
  description = "A mapping of keys to values required in the task definition template"
}

#-------------------------#
# Fargate Variables       #
#-------------------------#
variable "fargate_cpu" {
  description = "Describe CPU values for Fargate launch type"
}

variable "fargate_memory" {
  description = "Describe memory values for Fargate launch type"
}

#-------------------------#
# Networking Variables    #
#-------------------------#
variable "ecs_task_execution_role_arn" {
  description = "The ARN of the ECS task execution role"
}
variable "ecs_task_role_arn" {
  description = "The ARN of the ECS task role"
}
variable "vpc_id" {
  description = "VPC ID"
}
variable "private_subnet_ids" {
  description = "List of private subnets ids used in VPC"
}
variable "security_group_ids" {
  description = "List of security group ids"
}

#-------------------------#
# Cloudwatch Variables    #
#-------------------------#
variable "log_group_prefixes" {
  description = "Mapping of log group prefix to the Cloudwatch log group destination where {prefix}_log_group and {prefix}_log_stream are used in the task definition"
}

#------------------#
# ALB Variables    #
#------------------#
variable "enable_alb" {
  description = "Whether this service should be configured to attach a Target Group"
  default = false
}

variable "alb_service_container_name" {
  description = "Container name for the container connected to the ALB"
  default     = "N/A"
  validation {
    condition = var.alb_service_container_name != "N/A" || !var.enable_alb
    error_message = "Requires alb_service_container_name because ALB service"
  }
}

variable "alb_container_port" {
  description = "Port the ECS service is listening to"
  default     = "N/A"
  validation {
    condition     = var.alb_container_port != "N/A" || !var.enable_alb
    error_message = "Requires alb_container_port because ALB service"
  }
}

variable "health_check_path" {
  description = "Path on the service to use as a healthcheck"
  default     = "N/A"
  validation {
    condition     = var.health_check_path != "N/A" || !var.enable_alb
    error_message = "Requires health_check_path because ALB service"
  }
}

