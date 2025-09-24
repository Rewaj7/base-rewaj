resource "aws_alb" "app" {
  name                             = "${var.env}-load-balancer"
  internal                         = false
  security_groups                  = [aws_security_group.alb.id]
  enable_cross_zone_load_balancing = true
  subnets                          = data.aws_subnets.public.ids
}

resource "aws_alb_listener" "http" {
  load_balancer_arn = aws_alb.app.arn
  protocol          = "HTTP"
  port              = local.open_ports["HTTP"]
  default_action {
    target_group_arn = module.service.target_group_arn
    type             = "forward"
  }
}

resource "aws_security_group" "alb" {
  name = "alb-sg-${var.env}"
  description = "Security group for ALB"
  vpc_id      = data.aws_vpc.vpc.id

  dynamic "ingress" {
    for_each = local.ingress_ports
    iterator = port
    content {
      from_port   = port.value
      to_port     = port.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  dynamic "egress" {
    for_each = local.egress_ports
    iterator = port
    content {
      from_port   = port.value
      to_port     = port.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
}

locals {
  ingress_ports = [local.open_ports["HTTP"], local.open_ports["HTTPS"]]
  egress_ports = [local.open_ports["FASTAPI"]]

  open_ports = {
    HTTP       = 80
    HTTPS      = 443
    FASTAPI    = 8000
  }
}