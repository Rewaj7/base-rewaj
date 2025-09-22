resource "aws_vpc" "vpc" {
  cidr_block           = cidrsubnet(var.cidr_block, 0, 0)
  enable_dns_support   = true
  enable_dns_hostnames = true
}