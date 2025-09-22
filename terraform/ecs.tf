module "ecs" {
  source = "./modules/ecs"
  //General Variables
  env        = var.env

  //VPC Variables
  vpc_id     = var.vpc_id
}