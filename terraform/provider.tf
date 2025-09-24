terraform {
  backend "s3" {
  }
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}
provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Environment = var.env
      Configuration = "base-rewaj/terraform"
    }
  }
}

data "aws_caller_identity" "current" {}
