variable "key_rotation" {
    type = object({
      enable = bool
      deletion_window = number
    })
  default = {
    enable = false
    //if enable is false then set delettion window to null
    deletion_window = 20

  }
}
variable "kms_policy" {
  type = string
}