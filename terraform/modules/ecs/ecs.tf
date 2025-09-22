resource "aws_ecs_cluster" "app_cluster" {
  name = "rewaj-cb-${var.env}"
}
