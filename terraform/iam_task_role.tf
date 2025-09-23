resource "aws_iam_role" "ecs_task" {
  name        = "api-ecs-task-${var.env}"
  description = "Role allowing containerized application to call others AWS services"
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        Sid : "",
        Effect : "Allow",
        Principal : {
          "Service" : ["ecs.amazonaws.com","ecs-tasks.amazonaws.com"]
        },
        Action : "sts:AssumeRole"
      }
    ]
  })
}

data "aws_iam_policy" "cloudwatch_full" {
  arn = "arn:aws:iam::aws:policy/CloudWatchFullAccess"
}

resource "aws_iam_role_policy_attachment" "cloudwatch_full_attachment" {
  role       = aws_iam_role.ecs_task.name
  policy_arn = data.aws_iam_policy.cloudwatch_full.arn
}

data "aws_iam_policy" "ssm_read_only" {
  arn = "arn:aws:iam::aws:policy/AmazonSSMReadOnlyAccess"
}

resource "aws_iam_role_policy_attachment" "ssm_task_attachment" {
  role       = aws_iam_role.ecs_task.name
  policy_arn = data.aws_iam_policy.ssm_read_only.arn
}

data "aws_iam_policy" "ssm_managed" {
  arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_role_policy_attachment" "ecs_ssm" {
  role       = aws_iam_role.ecs_task.name
  policy_arn = data.aws_iam_policy.ssm_managed.arn
}

data "aws_iam_policy" "s3_read" {
  arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}

resource "aws_iam_role_policy_attachment" "s3_read" {
  role       = aws_iam_role.ecs_task.name
  policy_arn = data.aws_iam_policy.s3_read.arn
}

resource "aws_iam_policy" "sns_publish_policy" {
  name        = "ECS_SNS_Publish_Policy"
  description = "Allow ECS task to publish messages to SNS topic"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "sns:Publish"
        Resource = aws_sns_topic.notify_topic.arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_role_sns" {
  role       = aws_iam_role.ecs_task.name
  policy_arn = aws_iam_policy.sns_publish_policy.arn
}