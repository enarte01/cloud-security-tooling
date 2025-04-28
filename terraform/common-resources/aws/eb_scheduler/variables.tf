variable "schedule_group" {
  type = string
  default = ""
}
variable "schedule_name" {
    type = string
  
}
variable "schedule_expr" {
  type = string
  default = null
}
variable "flexible_time" {
    type = map({
      mode = string
      max_window = optional(string)
      //TODO add validation if mode is off
    })
  
}
variable "target" {
    type = list(object(
      {
        arn = string
        role_arn = string
        dead_letter_config = optional(object)
        input = optional(object)
        retry_policy = optional(object)
        //templated targets

      }
    ))
    validation {
      condition = length(var.target) == 1
      error_message = "target length must be 1"
    }
    
}