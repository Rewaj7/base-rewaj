#---------------------#
# Common Variables    #
#---------------------#
variable "env" {
  description = "Environment for application mainly used for prefixing resource names"
  default = "dev"
}

variable "aws_region" {
  default = "eu-west-1"
}

#---------------------#
# VPC Variables       #
#---------------------#
variable "vpc_remote_backend_bucket" {
  description = ""
  default = "devops-assignment-logs-19-08"
}

variable "vpc_remote_backend_file" {
  description = ""
  default = "rewaj-base-tf/rewaj-base-vpc-dev.tfstate"
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