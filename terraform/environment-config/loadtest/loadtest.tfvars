//Common
env = "loadtest"
ecr_tag = "stagng"
aws_region = "eu-west-1"

//VPC
vpc_remote_backend_config = {
  bucket = "devops-assignment-logs-19-08"
  key    = "rewaj-base-tf/rewaj-base-vpc-staging.tfstate"
  region = "eu-west-1"
}

//ECS
desired_count = 1
fargate_cpu = 256
fargate_memory = 512