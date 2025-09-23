resource "aws_vpc" "vpc" {
  cidr_block           = cidrsubnet(var.cidr_block, 0, 0)
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name        = "${var.env}-vpc"
  }
}


locals {
  subnets_cidr = [
    for i in range(length(data.aws_availability_zones.available)) : cidrsubnet(var.cidr_block, 4, i)
  ]

  public_subnets  = slice(
    local.subnets_cidr,
    0,
    length(data.aws_availability_zones.available)
  )

  private_subnets = slice(
    local.subnets_cidr,
    length(data.aws_availability_zones.available.names),
    length(data.aws_availability_zones.available.names) * 2
  )
}