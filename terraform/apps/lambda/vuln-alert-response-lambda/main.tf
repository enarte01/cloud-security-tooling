//scheduler
//lambda
//sns

module "lambda" {
  source              = "../../../modiules/aws/lambda"
  function_name       = "${local.extra_tags.app-name}-${local.deployed_tags.project-name}-lambda-${local.deployed_tags.env}"
  role_name           = "${local.extra_tags.app-name}-${local.deployed_tags.project-name}-lambda-role-${local.deployed_tags.env}"
  handler             = local.handler
  runtime             = local.runtime
  iam_policy_name     = "${local.extra_tags.app-name}-${local.deployed_tags.project-name}-iam-policy-${local.deployed_tags.env}"
  s3_bucket           = "${local.extra_tags.app-name}-${local.deployed_tags.project-name}-s3-bucket-${local.deployed_tags.env}"
  s3_key              = local.s3_key
  assume_role_policy  = local.assume_role_policy
  iam_policy          = local.iam_policy
  bucket_policy       = local.bucket_policy
  kms_policy          = local.kms_policy
  layer_name          = "${local.extra_tags.app-name}-${local.deployed_tags.project-name}-layer-${local.deployed_tags.env}"
  compatible_runtimes = local.compatible_runtimes
  create_layer        = true
  create_bucket       = true
  layer_filename = local.layer_filename
  log_group = "${local.extra_tags.app-name}-${local.deployed_tags.project-name}-log-group-${local.deployed_tags.env}"
  s3_object_source = local.s3_object_source
}

module "events_trigger" {
  source           = "../../../common-resources/aws/eb_events"
  target_id        = "${local.extra_tags.app-name}-${local.deployed_tags.project-name}-event-target-${local.deployed_tags.env}"
  event_rule_state = local.event_rule_state
  event_rule_name  = "${local.extra_tags.app-name}-${local.deployed_tags.project-name}-event-rule-${local.deployed_tags.env}"
  event_pattern    = local.event_pattern
  tags             = local.deployed_tags
  target_arn = module.lambda.lambda_arn

}

resource "aws_lambda_permission" "trigger_lambda" {
  statement_id  = "AllowExecutionFromEvents"
  action        = "lambda:InvokeFunction"
  function_name = module.lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = module.events_trigger.event_rule_arn
}
