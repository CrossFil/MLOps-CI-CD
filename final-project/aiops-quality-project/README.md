# MLOps AI-Quality Project: Drift Detection & Auto-Retraining
This repository contains a full-cycle MLOps project for a machine learning inference service with automated drift detection and self-healing (retraining) capabilities.

## Infrastructure Description
The project is built using a modern cloud-native stack:

- Inference Engine: FastAPI service wrapped in a Docker container.

- Drift Detection: Alibi Detect (Kolmogorov-Smirnov test) integrated into the inference logic.

- Orchestration: Kubernetes (K8s) for container management.

- Deployment (GitOps): ArgoCD synchronizes the state between this Git repo and the cluster using Helm charts.

- Monitoring: Prometheus (metrics) and Grafana (dashboards).

- Logging: Loki + Promtail to collect and analyze stdout logs.

- CI/CD: GitHub Actions for model retraining, Docker image building, and automatic Helm chart updates.

## How to Run the Project
### 1. Prepare Kubernetes Environment: Ensure you have a running K8s cluster and kubectl configured.

### 2. Install ArgoCD & Prometheus Stack:

- Deploy the Prometheus stack: `kubectl apply -f argocd/prometheus-app.yaml`

- Deploy the main application: `kubectl apply -f argocd/application.yaml`

### 3. Configure Secrets:
Create a GitHub PAT token in your cluster so the service can trigger the pipeline:

`Bash:
kubectl create secret generic github-api-token --from-literal=token=YOUR_GITHUB_TOKEN`

### 4. Access the Service:
Forward the port to your local machine:

`Bash:
kubectl port-forward svc/aiops-service-aiops 8000:80`
#
### How to Test a Request
You can send a standard inference request using `curl`:

`Bash:
curl -X POST http://localhost:8000/predict \
     -H "Content-Type: application/json" \
     -d '{"feature_value": 2.5}'`
     
The response will contain the `prediction`, a `drift` flag (boolean), and the current `model_version`.
#
### How to Check Logging
Logs are written to `stdout` in a structured format and collected by Loki.

1. Via CLI:

`Bash:
kubectl logs -l app=aiops-service`

2. Via Grafana:
Go to the "Explore" tab, select the Loki datasource, and use the query: `{app="aiops-service"}`. You will see every incoming request and its parameters.
#
### How to Check Detector Triggering
To simulate a Data Drift event, send a value that is significantly outside the reference range (the reference data is `[1.0, 5.0])`:

`Bash
curl -X POST http://localhost:8000/predict \
     -H "Content-Type: application/json" \
     -d '{"feature_value": 999.0}'`
     
What happens next:

1. The API response will show `"drift": true`.

2. In the logs, you will see: `WARNING:aiops-service:!!! DRIFT DETECTED !!!`.

3. The Prometheus metric `drift_detected_total` will increment.
#
### How to Check if Retrain-Pipeline Works
Once drift is detected, the service automatically triggers the GitHub Actions workflow.

1. Go to your GitHub repository's Actions tab.

2. You should see a new run titled MLOps Final Project CI/CD triggered by `repository_dispatch`.

3. The pipeline will:

- Run `model/train.py` to "update" the model.

- Build and push a new Docker image with a new tag.

- Crucially: It will automatically update `helm/values.yaml` with the new image tag.
#
### How to Update the Model
There are two ways to update the model:

1. Automatic:
     - Simply trigger a drift event (as described above), and the system will retrain and redeploy itself.

2. Manual:
     - Go to Actions -> MLOps Final Project CI/CD.
     - Click Run workflow to manually start the retraining process.

ArgoCD will detect the change in `values.yaml` and perform a rolling update in the cluster within minutes.
