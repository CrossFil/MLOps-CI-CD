# Local state storage configuration
terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}
