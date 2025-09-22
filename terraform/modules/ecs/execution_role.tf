resource "aws_iam_role" "ecs_task_execution" {
  name                = "ecs-task-execution-${var.env}"
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        Sid : "",
        Effect : "Allow",
        Principal : {
          "Service" : "ecs-tasks.amazonaws.com"
        },
        Action : "sts:AssumeRole"
      }
    ]
  })
}

data "aws_iam_policy" "ecs_task_execution" {
  arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy_attachment" "execution_policy_attachment" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = data.aws_iam_policy.ecs_task_execution.arn
}

resource "aws_iam_policy" "ecs-ssm" {
  name        = "ecs-ssm-${var.env}"
  description = "Provides access for ecs tasks to get parameters from parameter store"
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        Effect : "Allow",
        Action : [
          "ssm:GetParameters"
        ],
        Resource : [
          "arn:aws:ssm:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:parameter/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ssm_execution_attachment" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = aws_iam_policy.ecs-ssm.arn
}