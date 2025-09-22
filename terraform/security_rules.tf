resource "aws_security_group_rule" "allow-alb" {
  from_port                = local.open_ports["FASTAPI"]
  to_port                  = local.open_ports["FASTAPI"]
  protocol                 = "tcp"
  type                     = "ingress"
  security_group_id        = module.ecs.security_group_id
  source_security_group_id = module.alb.alb_sec_group_id
  description = "Allow ALB to send to ECS"
}

