variable "create_bucket" {
  type = bool
  default = false
}
variable "s3_bucket" {
  type = string
  default = ""
  //use validation
}
variable "function_name" {
    type = string
  
}
variable "bucket_policy" {
  type = string
}
variable "kms_key_arn" {
  type = string
  default = ""
}
variable "kms_policy" {
  type = string
}
//TODO
//if iam_for_lambda is default, set rest of iam vars to default
variable "iam_for_lambda" {
  type = string
  default = ""
}
variable "iam_policy" {
  type = string
}
variable "iam_policy_name" {
  type = string
}
variable "role_name" {
  type = string
}

variable "assume_role_policy" {
  type = string
}
variable "filename" {
  type = string
  default = ""
}
variable "image_uri" {
  type = string
  default = ""
}
variable "s3_key" {
  type = string
  default = ""
}
variable "s3_object_version" {
  type = string
  default = ""
}
variable "handler" {
  type = string
}
variable "runtime" {
  type = string
}
variable "timeout" {
  type = number
  default = 5
}
variable "memory_size" {
  type = number
  default = 2048
}
variable "ephemeral_storage" {
  type = number
  default = 4096
}
variable "layers" {
  type = list(string)
  default = []
}
variable "tags" {
  type = map(string)
  default = {
    "env" = "test",
    "project" = "my-project"
  }
}
variable "lambda_log_retention" {
  type = number
  default = 7
}
variable "create_layer" {
  type = bool
  default = false
}
variable "layer_name" {
  type = string
}
variable "compatible_runtimes" {
  type = list(string)
}