resource "aws_scheduler_schedule_group" "schedule_group" {
  name  = var.schedule_group
  count = var.schedule_group == "" || var.schedule_group == "default" ? 0 : 1

}

resource "aws_scheduler_schedule" "schedule" {
  name       = var.schedule_name
  group_name = var.schedule_group != "" || var.schedule_group != "default" ? aws_scheduler_schedule_group.schedule_group.id : "default"
  count      = var.schedule_expr == null ? 0 : 1
  flexible_time_window {
    mode                      = var.flexible_time.mode
    maximum_window_in_minutes = can(var.flexible_time.max_window) ? var.flexible_time.max_window : null
  }
  schedule_expression = var.schedule_expr
  
  dynamic "target" {
    for_each = var.target
    content {
      arn      = target.value["arn"]
      role_arn = target.value["role_arn"]
      input    = can(target.value["input"]) ? target.value["input"] : null
      //TODO
      //     dead_letter_config {

      //     }

      //     retry_policy {

      //     }

    }
  }

}
