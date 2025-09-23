resource "aws_sns_topic" "notify_topic" {
  name = "rewaj-base-topic-${var.env}"
}