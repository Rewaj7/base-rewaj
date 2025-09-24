#---------------------#
# Common Variables    #
#---------------------#
variable "env" {
  description = "Environment for application mainly used for prefixing resource names"
  default = "dev"
}

variable "ecr_tag" {
  description = "What latest-{ecr_tag} should be pulled from the ECR as ECS's image"
  default = "dev"
}

variable "aws_region" {
  default = "eu-west-1"
}

#---------------------#
# VPC Variables       #
#---------------------#
variable "vpc_remote_backend_config" {
  description = ""
  default = {
    bucket = "devops-assignment-logs-19-08"
    key    = "rewaj-base-tf/rewaj-base-vpc-dev.tfstate"
    region = "eu-west-1"
  }
}

#---------------------#
# ECS Variables       #
#---------------------#
variable "desired_count" {
  description = "The desired count of ECS tasks"
  default = 1
}
variable "fargate_cpu" {
  description = "Describe CPU values for Fargate launch type"
  default = 256
}
variable "fargate_memory" {
  description = "Describe memory values for Fargate launch type"
  default = 512
}