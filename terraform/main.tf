terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
provider "aws" { region = var.aws_region }

variable "aws_region" {
  type    = string
  default = "ap-south-1"
}

resource "aws_s3_bucket" "reports" {
  bucket_prefix = "data-protection-reports-"
}

resource "aws_dynamodb_table" "audit" {
  name         = "identity-audit"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "username"
  attribute { name = "username" type = "S" }
}

resource "aws_iam_role" "lambda" {
  name = "identity-reporting-lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = { Service = "lambda.amazonaws.com" },
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_lambda_function" "reporter" {
  function_name = "identity-reporting"
  role          = aws_iam_role.lambda.arn
  runtime       = "python3.12"
  handler       = "lambda_function.lambda_handler"
  filename      = "lambda.zip"
  source_code_hash = filebase64sha256("lambda.zip")
}

resource "aws_cloudwatch_log_group" "reports" {
  name = "/aws/lambda/identity-reporting"
}
