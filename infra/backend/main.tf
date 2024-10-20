provider "aws" {
  profile = "default"
  region  = "ap-south-1"
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>5.49.0"
    }
  }
}

resource "aws_s3_bucket" "state-bucket" {
  bucket = "tf-state-bucket-seiright"
  tags = {
    terraform = true
  }
}

resource "aws_s3_bucket_versioning" "state-bucket-versioning" {
  bucket = aws_s3_bucket.state-bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "state-bucket-encryption" {
  bucket = aws_s3_bucket.state-bucket.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_dynamodb_table" "state-dynamo-tale" {
  name             = "tf-state-dynamodb-table-seiright"
  billing_mode     = "PAY_PER_REQUEST"
  hash_key         = "LockID"
  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"
  attribute {
    name = "LockID"
    type = "S"
  }
  tags = {
    terraform = true
  }
}
