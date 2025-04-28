resource "aws_lambda_layer_version" "lambda_layer" {
  filename          = var.layer_bucket == "" ? var.filename : null
  s3_bucket         = var.filename == "" ? var.layer_bucket : null
  s3_key            = var.layer_bucket != ""? var.layer_bucket_key: null
  s3_object_version = var.layer_bucket != ""? var.layer_obj_version: null
  layer_name        = var.layer_name

  compatible_runtimes = var.compatible_runtimes
  //skip_destroy 
  //source_code_hash
}
