terraform {
  backend "s3" {
    bucket = "devops-assignment-logs-19-08"
    key    = "rewaj-base-tf/rewaj-base-vpc-dev.tfstate"
    region = "eu-west-1"
  }
}

provider "aws" {
  region = var.region
  default_tags {
    tags = {
      Environment   = var.env
      Configuration = "terraform_vpc"
    }
  }
}

data "aws_availability_zones" "available" {
  state = "available"
}