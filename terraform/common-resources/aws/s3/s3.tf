resource "aws_s3_bucket" "s3_bucket" {
  bucket = var.bucket_name
  //bucket_prefix
  //object_lock_enabled
  tags = var.tags
}

//required
resource "aws_s3_bucket_public_access_block" "bucket_acl" {
  bucket = aws_s3_bucket.s3_bucket.id

  block_public_acls       = var.bucket_pub_access["blck_pub_acls"]
  block_public_policy     = var.bucket_pub_access["blk_pub_policy"]
  ignore_public_acls      = var.bucket_pub_access["ign_pub_acls"]
  restrict_public_buckets = var.bucket_pub_access["restr_pub_buckets"]
}
//required
resource "aws_s3_bucket_policy" "bucket_policy" {
  bucket = aws_s3_bucket.s3_bucket.id
  policy = var.bucket_policy
}
//required
resource "aws_s3_bucket_server_side_encryption_configuration" "sse_encryption" {
  bucket = aws_s3_bucket.s3_bucket.id
  //TODO use expression to set kms master key param based on sse algorithm
  //create sse rule var object
  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = var.kms_key_arn
      sse_algorithm     = var.sse_algorithm
    }
  }
}
//optional
resource "aws_s3_bucket_versioning" "bucket_versioning" {
    count = var.versioning_status == "Disabled" ? 0: 1
    bucket = aws_s3_bucket.s3_bucket.id
    versioning_configuration {
        status = var.versioning_status
    }
}
//optional
resource "aws_s3_bucket_lifecycle_configuration" "bucket_lc" {
  count = var.lifecycle_rule == null? 0: 1
  bucket = aws_s3_bucket.s3_bucket.id

  dynamic "rule" {
    for_each = var.lifecycle_rule == null ? [] : [1]
    content {
        id = var.lifecycle_rule.id
        status = var.lifecycle_rule.status     
    } 
  }
}
//optional
//TODO expression for either or params for acl and access_control_policy
resource "aws_s3_bucket_acl" "bucket_acl" {
    count = var.bucket_acl == "private"? 0: 1
    depends_on = [aws_s3_bucket_public_access_block.bucket_acl]

    bucket = aws_s3_bucket.s3_bucket.id
    acl    = var.bucket_acl
}
//optional
resource "aws_s3_object" "object" {
  count = var.s3_key == ""? 0: 1
  bucket = aws_s3_bucket.s3_bucket.bucket
  key    = var.s3_key
  source = var.s3_object_source
}
//TODO
//aws_s3_bucket_cors_confguration
//aws_s3_bucket_replication_configuration
//aws_s3_bucket_object_lock_configuration

