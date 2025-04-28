output "lambda_arn" {
  value = aws_lambda_function.lambda.arn
}
output "function_name" {
  value = aws_lambda_function.lambda.function_name
}
output "layer_version_arn" {
  value = module.layer[0].layer_version_arn
}
output "layer_arn" {
  value = module.layer[0].layer_arn
}
//TODO use create_bucket and count to check bucket created
//output source s3 bucket
output "s3_bucket_arn" {
  value = module.s3_bucket[0].s3_bucket_arn
  
}
output "s3_bucket_name" {
  value = module.s3_bucket[0].s3_bucket_name
  
}