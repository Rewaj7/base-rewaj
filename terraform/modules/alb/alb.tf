resource "aws_alb" "app" {
  name                             = "${var.env}-load-balancer"
  internal                         = false
  security_groups                  = [aws_security_group.alb.id]
  enable_cross_zone_load_balancing = true
  subnets                          = var.public_subnets_ids
}

resource "aws_alb_listener" "http" {
  load_balancer_arn = aws_alb.app.arn
  protocol          = "HTTP"
  port              = var.open_ports["HTTP"]
  default_action {
    target_group_arn = var.aws_alb_target_group_api_arn
    type             = "forward"
  }
}
