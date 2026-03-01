# ArgoCD GitOps Project (Lesson 7)

## 1. Infrastructure Setup (Terraform)
To deploy the ArgoCD infrastructure on AWS EKS, run:
- `terraform init`
- `terraform apply -auto-approve`

## 2. Verify ArgoCD Status
Ensure all components are running in the `infra-tools` namespace:
- `kubectl get pods -n infra-tools`

## 3. Access ArgoCD UI
To access the web interface:
1. Port-forward the server: 
   `kubectl port-forward svc/argocd-server -n infra-tools 8080:443`
2. Open in browser: `https://localhost:8080`
3. **Username:** `admin`
4. **Password:** Get it using:
   `kubectl -n infra-tools get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d`

## 4. Verify Deployment
To check if the MLflow application is deployed and running:
- `kubectl get applications -n infra-tools`
- `kubectl get pods -n application`

## 5. Access MLflow Service
To open the MLflow UI:
- `kubectl port-forward svc/mlflow-app -n application 5000:5000`
- Visit: `http://localhost:5000`

## 6. Repository Link
The main application manifest can be found here:
[application.yaml](https://github.com/CrossFil/MLOps-CI-CD/blob/main/lesson-7/ArgoCD/application.yaml)
