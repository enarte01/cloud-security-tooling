output "schedule_arn" {
  value = aws_scheduler_schedule.schedule.arn
}
output "schedule_group" {
  value = aws_scheduler_schedule_group.schedule_group.id
}