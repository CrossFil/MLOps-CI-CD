# ArgoCD GitOps Project

## 1. Infrastructure Setup (Terraform)
To deploy the ArgoCD infrastructure on AWS EKS, run:
- `terraform init`
- `terraform apply -auto-approve`

## 2. Verify ArgoCD Status
Ensure all components are running in the `infra-tools` namespace:
- `kubectl get pods -n infra-tools`

<img width="613" height="155" alt="Снимок экрана 2026-03-01 в 13 13 17" src="https://github.com/user-attachments/assets/6c4c43c2-322f-4c32-b67c-3feb989264f3" />



## 3. Access ArgoCD UI
To access the web interface:
1. Port-forward the server: 
   `kubectl port-forward svc/argocd-server -n infra-tools 8080:443`
2. Open in browser: `https://localhost:8080`
3. **Username:** `admin`
4. **Password:** Get it using:
   `kubectl -n infra-tools get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d`

<img width="1412" height="740" alt="Снимок экрана 2026-03-01 в 11 31 07" src="https://github.com/user-attachments/assets/fa479e8b-87ba-471c-9f1d-350520b7ab3d" />


## 4. Verify Deployment
To check if the MLflow application is deployed and running:
- `kubectl get applications -n infra-tools`
- `kubectl get pods -n application`

  <img width="534" height="134" alt="Снимок экрана 2026-03-01 в 13 15 29" src="https://github.com/user-attachments/assets/16aa61ce-1e06-41c5-88f7-9c7fca323243" />


## 5. Access MLflow Service
To open the MLflow UI:
- `kubectl port-forward svc/mlflow-app -n application 5000:5000`
- Visit: `http://localhost:5000`

  
<img width="1388" height="637" alt="Снимок экрана 2026-03-01 в 11 24 06" src="https://github.com/user-attachments/assets/77bb1dbf-f566-4639-8f82-cce30d7ff557" />

## 6. Repository Link
The main application manifest can be found here:
[application.yaml](https://github.com/CrossFil/MLOps-CI-CD/main/lesson-7/ArgoCD/application.yaml)
