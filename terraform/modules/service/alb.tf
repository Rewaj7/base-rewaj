resource "aws_alb_target_group" "target_group" {
  name_prefix = "cb-tg"
  vpc_id      = var.vpc_id
  protocol    = "HTTP"
  port        = var.backend_listen_port
  target_type = "ip"

  health_check {
    path                = var.health_check_path
  }
}