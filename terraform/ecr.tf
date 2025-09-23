locals {
  ecr_name = "rewaj_base_ecr"
}

data "aws_ecr_repository" "ecr" {
  name = local.ecr_name
}