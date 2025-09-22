locals {
  ecr_name = ""
}

data "aws_ecr_repository" "ecr" {
  name = local.ecr_name
}