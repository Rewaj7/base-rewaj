module "service" {
  source = "./modules/service"
  //Common Variables
  service_name = "rewaj-base"
  env = var.env

  //ECS Variables
  cluster_arn = aws_ecs_cluster.app_cluster.arn
  desired_count = var.desired_count
  environment_vars = local.environment_variables
  ssm_secrets = local.secrets
  template_file_path = "${path.cwd}/templates/task_definition.json.tpl"
  template_inputs = local.template_input

  //Fargate Variables
  fargate_cpu = var.fargate_cpu
  fargate_memory = var.fargate_memory

  //Networking Variables
  ecs_task_role_arn = aws_iam_role.ecs_task.arn
  ecs_task_execution_role_arn = aws_iam_role.ecs_task_execution.arn
  vpc_id = data.aws_vpc.vpc.id
  private_subnet_ids = data.aws_subnets.private.ids
  security_group_ids = [aws_security_group.ecs_default.id]

  //Cloudwatch Variables
  log_group_prefixes = {
    "fastapi": "rewaj-base/fastapi/${var.env}"
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
    aws_region = var.aws_region,
    account_id = data.aws_caller_identity.current.account_id,
    alb_container_name = local.alb_container_name
  }
}