
resource "aws_cloudwatch_event_rule" "event_rule" {
  //count
  name = var.event_rule_name

  schedule_expression = var.event_pattern == "" ? var.schedule_expr : null
  event_pattern       = var.schedule_expr == "" ? var.event_pattern : null
  event_bus_name      = var.event_bus_name
  //role_arn = var.role_arn
  state = var.event_rule_state
  tags  = var.tags
  //force_destroy
}

resource "aws_cloudwatch_event_target" "event_target" {
  target_id = var.target_id
  rule      = aws_cloudwatch_event_rule.event_rule.name
  arn       = var.target_arn
  role_arn  = var.target_role_arn != ""? var.target_role_arn: null

  //dead_letter_config
  //retry_policy
  //input
  //input_path
  //input_transformer
  event_bus_name = var.event_bus_name
}
