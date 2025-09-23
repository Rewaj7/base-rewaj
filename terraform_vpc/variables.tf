variable "env" {
  default = "dev"
}

variable "region" {
  default = "eu-west-1"
}

variable "cidr_block" {
  description = "CIDR block for the VPC"
  default = "172.31.0.0/16"
}