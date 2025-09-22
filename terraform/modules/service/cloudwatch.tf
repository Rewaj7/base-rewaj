resource "aws_cloudwatch_log_group" "log_groups" {
  for_each          = var.log_group_prefixes
  name              = each.value
  retention_in_days = 14
}

resource "aws_cloudwatch_log_stream" "log_streams" {
  for_each       = var.log_group_prefixes
  name           = "rewaj-cb-${each.key}-stream"
  log_group_name = aws_cloudwatch_log_group.log_groups[each.key].name
}

locals {
  log_group_inputs = {
    for log_prefix, log_destination in var.log_group_prefixes:
      "${log_prefix}_log_group" => aws_cloudwatch_log_group.log_groups[log_prefix].name
  }
  log_stream_inputs = {
    for log_prefix, log_destination in var.log_group_prefixes:
      "${log_prefix}_log_stream" => aws_cloudwatch_log_stream.log_streams[log_prefix].name
  }
}
