provider "aws" {
  profile = "default"
  region  = "ap-south-1"
}


terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "tf-state-bucket-seiright"
    key            = "terraform.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "tf-state-dynamodb-table-seiright"
    encrypt        = true
  }
}

module "eks" {
  source       = "./eks"
  cluster_name = "eks-cluster-seiright"
}

