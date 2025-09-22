output "ecs_task_execution_arn" {
  value = aws_iam_role.ecs_task_execution.arn
}

output "ecs_task_arn" {
  value = aws_iam_role.ecs_task.arn
}

output "ecs_cluster_arn" {
  value = aws_ecs_cluster.app_cluster.arn
}

output "security_group_id" {
  value = aws_security_group.ecs_default.id
}
