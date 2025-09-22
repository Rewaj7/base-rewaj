#---------------------#
# Common Variables    #
#---------------------#
variable "env" {
  description = "Environment for application mainly used for prefixing resource names"
}

#---------------------#
# VPC Variables       #
#---------------------#
variable "vpc_id" {
  description = "VPC ID the application should reside in"
}

#---------------------#
# ECS Variables       #
#---------------------#
variable "desired_count" {
  description = "The desired count of ECS tasks"
}
variable "fargate_cpu" {
  description = "Describe CPU values for Fargate launch type"
}
variable "fargate_memory" {
  description = "Describe memory values for Fargate launch type"
}