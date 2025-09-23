resource "aws_ecs_cluster" "app_cluster" {
  name = "rewaj-cb-${var.env}"
}

resource "aws_security_group" "ecs_default" {
  name   = "ecs-sg-${var.env}"
  vpc_id = data.aws_vpc.vpc.id

  # Outbound traffic
  egress {
    from_port = 0
    protocol  = "-1"
    to_port   = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port                = local.open_ports["FASTAPI"]
    to_port                  = local.open_ports["FASTAPI"]
    protocol                 = "tcp"
    security_groups        = [aws_security_group.alb.id]
    description              = "Allow ALB to send to ECS"
  }
}