output "bucket_name" {
  value = aws_s3_bucket_logging.logging_bucket.id
}