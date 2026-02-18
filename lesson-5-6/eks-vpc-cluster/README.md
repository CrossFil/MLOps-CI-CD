# AWS EKS Cluster Deployment via Terraform Modules

This project automates the deployment of a production-ready AWS infrastructure using a modular Terraform approach.

## Architecture Overview
The infrastructure is decoupled into two primary logical modules:
- **VPC Module**: Provisions a customized Virtual Private Cloud with public and private subnets across multiple Availability Zones, including a NAT Gateway for secure egress traffic from private nodes.
- **EKS Module**: Deploys an Amazon Elastic Kubernetes Service (EKS) cluster (version 1.29) with managed node groups.

## Project Structure
```text
eks-vpc-cluster/
├── main.tf           # Root configuration orchestrating modules
├── variables.tf      # Global variables
├── vpc/              # Networking layer configuration
│   ├── main.tf
│   ├── outputs.tf
│   └── variables.tf
└── eks/              # Kubernetes cluster layer configuration
    ├── main.tf
    ├── variables.tf
    └── outputs.tf
Managed Node Groups
The cluster utilizes AWS Managed Node Groups with t3.micro instances to stay within cost-effective boundaries:

cpu_nodes: Dedicated for general-purpose workloads.

gpu_nodes: Provisioned for specialized compute tasks (logical separation).

Verification Steps
Post-deployment, connectivity was verified using the following steps:

Update Kubeconfig:
`aws eks --region eu-central-1 update-kubeconfig --name mlops-eks`

Verify Node Status:
`kubectl get nodes`
All nodes confirmed in 'Ready' state before teardown.

Resource Cleanup
To avoid unnecessary AWS charges (specifically for EKS Control Plane and NAT Gateway), the environment is decommissioned using:
`terraform destroy`
