variable "sns_topic_name" {
  type = string

}
variable "sns_topic_policy" {
    type = object({
        name = ""
    })
}
variable "sns_topic_kms_key" {
  type = string
}
variable "delivery_policy" {
  type = object({
    name = ""
  })
}
variable "tags" {
  type = map(string)
  default = {
    "env" = "test",
    "project" = "my-project"
  }
}
variable "topic_arn" {
  type = string
  default = ""
}
variable "protocol" {
  type = string
}
variable "endpoint" {
  type = string
}
variable "raw_message" {
  type = bool
  default = true
}
variable "filter_policy" {
  type = object({
    name = ""
  })
  default = null
}
variable "filter_policy_scope" {
  type = object({
    name = ""
  })
  default = null
}
variable "fifo_topic" {
  type = bool
  default = false
}
variable "content_deduplication" {
  type = bool
  default = true
}