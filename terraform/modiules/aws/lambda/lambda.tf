module "s3_bucket" {
  count         = var.create_bucket ? 1 : 0
  source        = "../../../common-resources/aws/s3"
  bucket_name   = "${var.function_name}-bucket"
  bucket_policy = var.bucket_policy
  kms_key_arn   = var.kms_key_arn != "" ? var.kms_key_arn : module.kms_key[0].kms_key_arn
}
module "kms_key" {
  count      = var.kms_key_arn == "" ? 1 : 0
  source     = "../../../common-resources/aws/kms"
  kms_policy = var.kms_policy
}
module "execution_role" {
  count              = var.iam_for_lambda == "" ? 1 : 0
  source             = "../../../common-resources/aws/iam_role"
  iam_policy         = var.iam_policy
  iam_policy_name    = var.iam_policy_name
  role_name          = var.role_name
  assume_role_policy = var.assume_role_policy
}
module "log_group" {
  source            = "../../../common-resources/aws/cw_log"
  log_group         = "aws/lambda/${var.function_name}"
  retention_in_days = var.lambda_log_retention
}

//TODO code signing


module "layer" {
  count               = var.create_layer ? 1 : 0
  source              = "../../../common-resources/aws/lambda_layer"
  layer_name          = var.layer_name
  compatible_runtimes = var.compatible_runtimes
  filename = "kerrjek.zip"
}

resource "aws_lambda_function" "lambda" {

  filename          = var.filename != "" || var.s3_bucket == "" && var.image_uri == "" ? var.filename : null
  image_uri         = var.image_uri != "" || var.filename == "" && var.s3_bucket == "" ? var.image_uri : null
  s3_bucket         = var.s3_bucket != "" || var.filename == "" && var.image_uri == "" ? var.s3_bucket : null
  s3_key            = var.s3_bucket != "" ? var.s3_key : null
  s3_object_version = var.s3_key != "" && var.s3_object_version != "" ? var.s3_object_version : null
  function_name     = var.function_name
  role              = var.iam_for_lambda != "" ? var.iam_for_lambda : module.execution_role[0].iam_role_arn
  handler           = var.handler
  //code_signing_config_arn
  //architectures
  //source_code_hash
  runtime     = var.runtime
  timeout     = var.timeout
  memory_size = var.memory_size
  ephemeral_storage {
    size = var.ephemeral_storage
  }
  //kms_key_arn = var.kms_key_arn if env variables is set
  //logging_config
  layers = var.layers != [] && var.create_layer == false ? var.layers : [module.layer[*].layer_version_arn]
  //vpc_config 
  //dead_letter_config TODO
  //environment TODO

  //file_system_config
  //image_config
  //tracing_config
  //package_type
  tags = var.tags
  depends_on = [
    module.log_group
  ]
}
