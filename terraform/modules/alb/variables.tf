#------------------#
# General Variables#
#------------------#
variable "env" {
  description = "Environment (dev/staging/prod)"
  type = string
}

#------------------#
# VPC Variables    #
#------------------#
variable "vpc_id" {
  description = "VPC ID"
  type = string
}

variable "public_subnets_ids" {
  description = "Public subnets ids list for the above VPC where ALB will be provisioned"
  type = list(string)
}


#------------------#
# ALB Variables    #
#------------------#
variable "open_ports" {
  description = "Mapping of port name to port number"
  type = map(number)
}

variable "aws_alb_target_group_api_arn" {
  description = "ARN for the default service ALB Target Group"
  type = string
}
