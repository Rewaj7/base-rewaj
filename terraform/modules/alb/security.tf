resource "aws_security_group" "alb" {
  name = "alb-sg-${var.env}"
  description = "Security group for ALB"
  vpc_id      = var.vpc_id

  dynamic "ingress" {
    for_each = local.standard_ingress_ports
    iterator = port
    content {
      from_port   = port.value
      to_port     = port.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  dynamic "egress" {
    for_each = local.standard_egress_ports
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
  standard_ingress_ports = [var.open_ports["HTTP"], var.open_ports["HTTPS"]]
  standard_egress_ports = [var.open_ports["FASTAPI"]]
}
