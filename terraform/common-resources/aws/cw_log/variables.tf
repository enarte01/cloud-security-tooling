variable "log_group" {
  type = string
}
variable "tags" {
  type = map(string)
  default = {
    "env" = "test",
    "project" = "my-project"
  }
}
variable "retention_in_days" {
  type = number
  default = null
}
variable "kms_key_id" {
  type = string
  default = null
}