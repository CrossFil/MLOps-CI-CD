# MLOps Training Automation Pipeline

This project automates an ML training workflow using **AWS Lambda**, **AWS Step Functions**, and **Terraform**, with a CI/CD pipeline powered by **GitHub Actions**.

## Project Structure
* `lambda/`: Contains Python code for data validation and metric logging.
* `terraform/`: Infrastructure as Code (IaC) to deploy AWS resources.
* `.github/workflows/`: Automation script for the CI/CD pipeline.

---

## 1. How to Build Lambda Packages
Before deploying with Terraform, the Python scripts must be packaged into `.zip` archives.

Run these commands in the `lambda/` directory:
`bash:
zip validate.zip validate.py
zip log_metrics.zip log_metrics.py`

## 2. Infrastructure Deployment (Terraform)
To deploy the IAM roles, Lambda functions, and the Step Function state machine:

Navigate to the terraform/ folder:

`Bash:
cd terraform`
Initialize Terraform:

`Bash:
terraform init`
Apply the configuration:

`Bash:
terraform apply -auto-approve`

## 3. Manual Execution of Step Function
You can trigger the pipeline manually via the AWS CLI:

`Bash:
aws stepfunctions start-execution \
  --state-machine-arn "YOUR_STATE_MACHINE_ARN" \
  --input '{"source": "manual-trigger"}'`
Or via the AWS Console:

Go to Step Functions -> State machines.

Select `mlops-automation-pipeline.`

Click Start execution.

## 4. GitHub Actions CI/CD
The pipeline is automatically triggered on every push to the main branch.

Required Secrets

To allow GitHub to communicate with AWS, add the following secrets in Settings > Secrets and variables > Actions:

- AWS_ACCESS_KEY_ID: Your AWS Access Key.

- AWS_SECRET_ACCESS_KEY: Your AWS Secret Key.

Workflow Verification

Once the workflow runs, you can see the result in the Actions tab of this repository.

<img width="1317" height="763" alt="Снимок экрана 2026-03-09 в 10 10 26" src="https://github.com/user-attachments/assets/4dad02be-6faa-4508-b3eb-cbf73f40e92f" />

## 5. Sample Input JSON
The Step Function accepts a JSON input to track the source of the trigger:

JSON
`{
  "source": "github-actions",
  "commit": "a1b2c3d"
}`

## 6. Pipeline Execution Results
When the Step Function completes, all steps in the visual workflow should turn green.
<img width="1317" height="712" alt="Снимок экрана 2026-03-09 в 10 11 43" src="https://github.com/user-attachments/assets/cb680df4-756e-4206-8691-7ae1af365731" />
<img width="1317" height="712" alt="Снимок экрана 2026-03-09 в 10 19 10" src="https://github.com/user-attachments/assets/88fcc93d-6f7a-4030-9704-e1b493ca7fee" />
<img width="1317" height="712" alt="Снимок экрана 2026-03-09 в 10 33 09" src="https://github.com/user-attachments/assets/d7125e16-a63f-4772-9992-afabfbd747ef" />

