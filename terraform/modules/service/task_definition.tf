resource "aws_ecs_task_definition" "task_definition" {
  family                   = "rewaj-cb-${var.env}"
  execution_role_arn       = var.ecs_task_execution_role_arn
  task_role_arn            = var.ecs_task_role_arn
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  container_definitions    = templatefile(var.template_file_path, local.template_input)
  skip_destroy             = true
}

locals {
  template_input = merge(
    local.log_group_inputs,
    local.log_stream_inputs,
    var.template_inputs,
    {
      environment_variables = [
        for env_key, env in var.environment_vars :
          { name = env_key, value = tostring(env) }
      ]
    },
    {
      ssm_secrets = [
        for env_key, ssm_value in var.ssm_secrets :
          { name = env_key, value = tostring(ssm_value) }
      ]
    }
  )
}
