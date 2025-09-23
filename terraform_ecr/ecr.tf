terraform {
  backend "s3" {
    bucket = "devops-assignment-logs-19-08"
    key    = "rewaj-base-tf/rewaj-base-ecr-dev.tfstate"
    region = "eu-west-1"
  }
}

provider "aws" {
  region = "eu-west-1"
}

resource "aws_ecr_repository" "ecr_repo" {
  name = "rewaj_base_ecr"
}