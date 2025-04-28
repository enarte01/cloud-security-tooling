resource "aws_iam_role" "iam_role" {
  name = var.role_name

  assume_role_policy = var.assume_role_policy
  //path
  max_session_duration = var.max_session
  //permissions_boundary
  tags = var.tags
}

//required
resource "aws_iam_role_policy_attachment" "policy_attach" {
  role       = aws_iam_role.iam_role.name
  policy_arn = var.policy_arn == "" ? aws_iam_policy.iam_policy[0].arn : var.policy_arn
}
//aws_iam_role_policy (inline)
//aws_iam_policy (managed)
//optional
resource "aws_iam_policy" "iam_policy" {
  count  = var.policy_arn == "" ? 1 : 0
  name   = var.iam_policy_name
  policy = var.iam_policy
}
//terraform managed
//aws_iam_role_policy_attachments_exclusive
//TODO can inline and managed be stacked