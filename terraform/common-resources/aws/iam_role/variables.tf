variable "tags" {
  type = map(string)
  default = {
    "env" = "test",
    "project" = "my-project"
  }
}
variable "role_name" {
  type = string
}
variable "assume_role_policy" {
  type = string
}
variable "iam_policy" {
  type = string
}
variable "policy_arn" {
  type = string
  default = ""
}
variable "iam_policy_name" {
    type = string
  
}
variable "max_session" {
  type = number
  default = 3600
}
//create_inline ?