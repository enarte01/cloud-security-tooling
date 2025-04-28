variable "bucket_name" {
  type = string
}
variable "logging_bucket" {
  type = string
}
variable "logging_prefix" {
  type = string
  default = "logging/"
}