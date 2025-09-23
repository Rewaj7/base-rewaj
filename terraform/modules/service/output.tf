output "target_group_arn" {
  value = var.enable_alb ? aws_alb_target_group.target_group[0].arn : "N/A"
}
