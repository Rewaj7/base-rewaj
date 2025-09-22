resource "aws_security_group" "ecs_default" {
  name        = "ecs-sg-${var.env}"
  vpc_id      = var.vpc_id

  # Outbound traffic
  egress {
    from_port   = 0
    protocol    = "-1"
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}
