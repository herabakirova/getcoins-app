terraform {
  backend "s3" {
    bucket = "getcoins-hera-ohio"
    key    = "aws-infrastructure/terraform.tfstate"
    region = "us-east-2"
  }
}