variable "create_layer" {
  type = bool
  default = false
}
variable "filename" {
  type = string
  default = ""

}
variable "layer_bucket" {
  type = string
  default = ""
}
variable "layer_bucket_key" {
  type = string
  default = ""
}
variable "layer_obj_version" {
  type = string
  default = ""
}
variable "layer_name" {
  type = string
}
variable "compatible_runtimes" {
  type = list(string)
}