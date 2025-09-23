resource "aws_alb_target_group" "target_group" {
  count = var.enable_alb ? 1 : 0
  name_prefix = "cb-tg"
  vpc_id      = var.vpc_id
  protocol    = "HTTP"
  port        = var.alb_container_port
  target_type = "ip"

  health_check {
    path                = var.health_check_path
  }
}

locals {
  load_balancer_target_group_arns = var.enable_alb ? [aws_alb_target_group.target_group[0].arn] : []
}