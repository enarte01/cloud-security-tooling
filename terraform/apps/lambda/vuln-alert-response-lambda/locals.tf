data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}
data "aws_iam_policy_document" "lambda_policy" {
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",

    ]
    resources = ["arn:aws:logs:*:*:*"]
  }
  statement {

    actions = [
      "s3:GetObject",
      "s3:ListBucket",
    ]
    resources = [
      module.lambda.s3_bucket_arn,
      "${module.lambda.s3_bucket_arn}/*",
    ]
  }
  statement {

    actions = [
      "ecr:*"
    ]
    resources = ["*"]
  }
}
data "aws_iam_policy_document" "s3_bucket_policy" {
  statement {
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = [
      "s3:GetObject",
      "s3:ListBucket",
      "s3:GetObjectVersion",
      "s3:PutObject",
      "S3:PutObjectAcl"
    ]
    resources = [
      module.lambda.s3_bucket_arn,
      "${module.lambda.s3_bucket_arn}/*",
    ]
  }
}

data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "kms_policy" {
   statement {
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"]
    }

    actions = ["*"]
    resources = ["*"]
  }
  statement {
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = [data.aws_caller_identity.current.arn]
    }

    actions = ["kms:Create*",
          "kms:Describe*",
          "kms:Enable*",
          "kms:List*",
          "kms:Put*",
          "kms:Update*",
          "kms:Revoke*",
          "kms:GenerateDataKey",
          "kms:Disable*",
          "kms:Get*",
          "kms:Delete*",
          "kms:ScheduleKeyDeletion",
          "kms:CancelKeyDeletion"
          ]
    resources = ["*"]
  }
  
  statement {
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:ReEncrypt",
          "kms:GenerateDataKey",
          "kms:DescribeKey",
          "kms:CreateGrant"
    ]
    resources = ["*"]
  }


}
locals {
  extra_tags = {
    "app-name"     = "vuln-alert-response-lambda"
    "app-owner"    = "EdmundN"
    "cost-centre"  = "cpd-portfolio"
    "support-team" = "cpd-support"
    "org-unit"     = "cpd-portfolio"
    "env"          = var.env
  }
  deployed_tags      = merge(var.tags, local.extra_tags)
  handler            = "lambda_handler"
  runtime            = "python3.12"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
  iam_policy         = data.aws_iam_policy_document.lambda_policy.json
  bucket_policy      = data.aws_iam_policy_document.s3_bucket_policy.json
  kms_policy         = data.aws_iam_policy_document.kms_policy.json
  s3_key             = "${local.extra_tags.app-name}.zip"
  s3_object_source   = "${local.extra_tags.app-name}.zip"
  flexible_time = {
    "mode" = "OFF"
  }
  event_rule_state = "ENABLED"
  event_pattern = jsonencode({
    source = [
      "aws.inspector2",
      "aws.ecr"
    ]

    detail-type = [
      "Inspector2 Scan",
      "ECR Image Scan"
    ]
    detail = { "scan-status" : ["INITIAL_SCAN_COMPLETE", "COMPLETE"] }
  })
  compatible_runtimes = ["python3.11", "python3.12"]
}

//not used
data "aws_iam_policy_document" "events_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }
  }
}
//not used
data "aws_iam_policy_document" "events_policy" {
  statement {
    effect    = "Allow"
    actions   = ["lambda:InvokeFunction"]
    resources = [module.lambda.lambda_arn]
  }
}
