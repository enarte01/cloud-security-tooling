variable "bucket_name" {
    type = string

}
variable "tags" {
  type = map(string)
  default = {
    "env" = "test",
    "project" = "my-project"
  }
}
variable "bucket_pub_access" {
  type = map(bool)
  default = {
    "blck_pub_acls" = true,
    "blk_pub_policy" = true,
    "ign_pub_acls" = true,
    "restr_pub_buckets" = true
  }
}
variable "bucket_policy" {
    type = string
  
}
//TODO change tom resource
variable "versioning_status" {
  type = string
  validation {
    condition = contains(["Enabled", "Disabled", "Suspended"], var.versioning_status)
    error_message = "versioning status must be one of Enabled, Disabled, Suspened"
  }
  default = "Disabled" 
}
variable "lifecycle_rule" {
  type = list(object({}))
  default = null
}

variable "sse_algorithm" {
  type = string
  default = "aws:kms"
}
variable "kms_key_arn" {
  type = string
}
variable "bucket_acl" {
  type = string
  validation {
    condition = contains(["private","public-read","public-read-write","aws-exec-read",
    "authenticated-read","bucket-owner-read","bucket-owner-full-control","log-delivery-write"], var.bucket_acl)
    error_message = "bucket acl is invalid"
  }
  default = "private" 
}
variable "s3_key" {
  type = string
  default = ""
}
variable "s3_object_source" {
  type = string
  default = ""
}