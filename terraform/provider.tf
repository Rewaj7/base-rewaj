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
  region = "eu-west-1"
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

