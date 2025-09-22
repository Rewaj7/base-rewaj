#------------------#
# General Variables#
#------------------#
variable "env" {
  description = "Environment"
}


#------------------#
# VPC Variables    #
#------------------#
variable "vpc_id" {
  description = "VPC ID to associate the Security Group. Likely all services within the cluster will use same SG"
}
