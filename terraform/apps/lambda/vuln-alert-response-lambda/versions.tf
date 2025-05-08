terraform {
  required_version = ">= 0.15"
  required_providers {
    aws = {
        source = "hashicorp/aws"
        version = "~> 5.94"
    }
  }
  backend "s3" {
    key = "lambda-state/tf-state"
    
  }
}