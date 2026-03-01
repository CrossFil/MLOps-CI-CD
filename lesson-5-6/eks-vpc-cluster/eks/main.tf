variable "vpc_id" {}
variable "subnet_ids" {}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = "mlops-eks"
  cluster_version = "1.29"

  vpc_id                         = var.vpc_id
  subnet_ids                     = var.subnet_ids
  cluster_endpoint_public_access = true

  eks_managed_node_groups = {
    cpu_nodes = {
      min_size     = 1
      max_size     = 1
      desired_size = 1
      instance_types = ["t3.micro"]
    }
    gpu_nodes = {
      min_size     = 1
      max_size     = 1
      desired_size = 1
      instance_types = ["t3.micro"]
    }
  }
}
