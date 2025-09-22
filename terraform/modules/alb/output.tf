output "alb_sec_group_id" {
  value = aws_security_group.alb.id
}

output "alb_dns_name" {
  value = aws_alb.app.dns_name
}