module "ecs" {
  source = "./modules/ecs"
  //General Variables
  env        = var.env

  //VPC Variables
  vpc_id     = data.aws_vpc.vpc.id
}