provider "aws" {
  region = "eu-central-1"
}

module "vpc" {
  source = "./vpc"
}

module "eks" {
  source     = "./eks"
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets
  depends_on = [module.vpc]
}
