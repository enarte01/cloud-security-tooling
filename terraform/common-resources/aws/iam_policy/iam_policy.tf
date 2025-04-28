/**
aws_iam_policy_attachment
The aws_iam_policy_attachment resource creates exclusive attachments of IAM policies. 
Across the entire AWS account, all of the users/roles/groups to which a single policy 
is attached must be declared by a single aws_iam_policy_attachment resource. 
This means that even any users/roles/groups that have the attached policy via any 
other mechanism (including other Terraform resources) will have that attached policy 
revoked by this resource. Consider aws_iam_role_policy_attachment, 
aws_iam_user_policy_attachment, or aws_iam_group_policy_attachment instead. 
These resources do not enforce exclusive attachment of an IAM policy.
**/
