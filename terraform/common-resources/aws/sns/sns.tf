
resource "aws_sns_topic" "sns_topic" {
  name  = var.sns_topic_name
  count = var.topic_arn == "" ? 0 : 1

  policy            = var.sns_topic_policy
  kms_master_key_id = var.sns_topic_kms_key
  delivery_policy   = var.delivery_policy

  tags = var.tags
  fifo_topic = var.fifo_topic
  content_based_deduplication = var.fifo_topic == true? var.content_deduplication : null
  //archive_policy
  //tracing_config
}

resource "aws_sns_topic_subscription" "sns_subscription" {
  topic_arn            = var.topic_arn == "" ? aws_sns_topic.sns_topic.arn : var.topic_arn
  protocol             = var.protocol
  endpoint             = var.endpoint
  filter_policy        = var.filter_policy
  filter_policy_scope  = var.filter_policy_scope
  raw_message_delivery = var.raw_message
  //delivery_policy only applies to http/s
  //redrive_policy
  //replay_policy
  //subscription_role_arn if firehose
  //confirmation_timeout_in_minutes 
}

//aws_sns_topic_data_protection_policy
//aws_sns_topic_policy
