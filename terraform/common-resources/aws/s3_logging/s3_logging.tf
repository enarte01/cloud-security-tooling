resource "aws_s3_bucket_logging" "logging_bucket" {
  bucket = var.bucket_name

  target_bucket = var.logging_bucket
  target_prefix = var.logging_prefix
}