resource "aws_kms_key" "kms_key" {
  enable_key_rotation     = var.key_rotation.enable
  deletion_window_in_days = var.key_rotation.deletion_window
  policy = var.kms_policy
}