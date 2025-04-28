variable "event_rule_name" {
  type = string
}
variable "event_pattern" {
  type = string
  default = ""
}
variable "schedule_expr" {
  type = string
  default = ""
}
variable "event_bus_name" {
  type = string
  default = "default"
}
variable "target_role_arn" {
  type = string
  default = ""
}
variable "event_rule_state" {
  type = string
  validation {
    condition = contains(["DISABLED", "ENABLED","ENABLED_WITH_ALL_CLOUDTRAIL_MANAGEMENT_EVENTS"],var.event_rule_state)
    error_message = "specify a valid state"
  }
}
variable "tags" {
  type = object({

  })
}
variable "target_id" {
  type = string
}