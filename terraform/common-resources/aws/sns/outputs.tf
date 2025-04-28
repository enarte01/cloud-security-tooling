output "topic_arn" {
  value = aws_sns_topic.sns_topic.arn
}

output "subscription_arn" {
    value = aws_sns_topic_subscription.sns_subscription.arn
  
}
output "pending_confirmation" {
  value = aws_sns_topic_subscription.sns_subscription.pending_confirmation
}

//confirmation_was_authenticated