module "service" {
  source = "./modules/service"
  //Common Variables
  service_name = "rewaj-cb"
  env = var.env

  //ECS Variables
  cluster_arn = module.ecs.ecs_cluster_arn
  desired_count = var.desired_count
  environment_vars = local.environment_variables
  ssm_secrets = local.secrets
  template_file_path = "${path.cwd}/templates/task_definition.json.tpl"
  template_inputs = local.template_input

  //Fargate Variables
  fargate_cpu = var.fargate_cpu
  fargate_memory = var.fargate_memory

  //Networking Variables
  ecs_task_role_arn = module.ecs.ecs_task_arn
  ecs_task_execution_role_arn = module.ecs.ecs_task_execution_arn
  vpc_id = var.vpc_id
  private_subnet_ids = data.aws_subnets.private.ids
  security_group_ids = [module.ecs.security_group_id]

  //Cloudwatch Variables
  log_group_prefixes = {
    "rack": "rewaj-cb/rack/${var.env}"
  }

  //ALB Variables
  alb_service_container_name = local.alb_container_name
  backend_listen_port = local.open_ports["FASTAPI"]
  health_check_path = "/health"
}


locals {
  alb_container_name = "rewaj-base-${var.env}"

  environment_variables = {
  }

  secrets = {
  }

  template_input = {
    env = var.env,
    image = "${data.aws_ecr_repository.ecr.repository_url}:latest-${var.env}",
    fastapi_port = local.open_ports["FASTAPI"]
    aws_region = data.aws_region.current.name,
    account_id = data.aws_caller_identity.current.account_id,
    alb_container_name = local.alb_container_name
  }
}