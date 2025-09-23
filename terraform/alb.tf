module "alb" {
  source = "./modules/alb"
  //General
  env = var.env

  //VPC
  vpc_id = data.aws_vpc.vpc.id
  public_subnets_ids = data.aws_subnets.public.ids

  //ALB
  open_ports = local.open_ports
  aws_alb_target_group_api_arn = module.service.target_group_arn
}

locals {
  open_ports = {
    HTTP       = 80
    HTTPS      = 443
    FASTAPI    = 8000
  }
}