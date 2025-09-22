resource "aws_ecs_service" "service" {
  name                    = "${var.service_name}-${var.env}"
  cluster                 = var.cluster_arn
  task_definition         = aws_ecs_task_definition.task_definition.family
  enable_execute_command  = true
  force_new_deployment    = true
  desired_count           = var.desired_count

  network_configuration {
    security_groups  = var.security_group_ids
    subnets          = var.private_subnet_ids
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_alb_target_group.target_group.arn
    container_name   = var.alb_service_container_name
    container_port   = var.backend_listen_port
  }

  capacity_provider_strategy {
    capacity_provider = "FARGATE"
    base              = 1
    weight            = 1
  }
}

