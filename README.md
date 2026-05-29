# MLOps Module — Summary

**Repository:** [CrossFil/MLOps-CI-CD](https://github.com/CrossFil/MLOps-CI-CD)  
**Final project:** `final-project/aiops-quality-project`

---

## What Was Studied

### Containerization
- Writing `Dockerfile` (multi-stage aware, slim base images)
- Docker Compose for local service orchestration
- Image tagging strategies (commit SHA as tag for traceability)

### CI/CD with GitHub Actions
- Workflow triggers: `push`, `workflow_dispatch`, `repository_dispatch` (event-driven from running service)
- Multi-step pipelines: checkout → Python setup → retrain → Docker build & push → Helm values update → auto-commit
- Secrets management: `DOCKERHUB_TOKEN`, `GITHUB_TOKEN`, `AWS_ACCESS_KEY_ID`

### Kubernetes & Helm
- Writing Kubernetes manifests: `Deployment`, `Service`, `ServiceMonitor`
- Helm chart structure: `Chart.yaml`, `values.yaml`, templated manifests
- Resource limits and requests (`cpu`, `memory`) in pod spec
- Environment variables injected from Kubernetes `Secret` objects

### GitOps with ArgoCD
- ArgoCD `Application` CRD: declarative sync between Git repo and cluster
- `automated` sync policy with `prune: true` and `selfHeal: true`
- Deploying the kube-prometheus-stack via ArgoCD from a Helm chart repository

### Monitoring with Prometheus & Grafana
- Exposing custom metrics via `prometheus_client` (`Counter`)
- Prometheus scrape configuration via pod annotations and `ServiceMonitor` CRD
- `PrometheusOperator`: deploying a `Prometheus` instance via CRD
- Grafana dashboards for service observability
- Log aggregation with Loki + Promtail (querying via `{app="aiops-service"}`)

### Serving ML Models with FastAPI
- REST API with Pydantic input schema (`BaseModel`)
- Startup event handler for loading model and drift detector
- `/predict` and `/metrics` endpoints
- Async HTTP calls with `httpx` to trigger external workflows

### Data Drift Detection
- **Alibi Detect** library: `KSDrift` (Kolmogorov-Smirnov test)
- Concept of reference data and p-value threshold (`p_val=0.05`)
- Inline drift detection on every inference request
- Automated retraining trigger via GitHub `repository_dispatch` event on drift

### Infrastructure as Code
- AWS Step Functions triggered from GitHub Actions (`deploy.yml`)
- Helm `values.yaml` as the single source of truth for image tags, updated automatically by CI

---

## Final Project: `aiops-quality-project`

A self-healing ML inference service with automated drift detection and continuous retraining.

### What the Service Does

A FastAPI application serves a regression model. On every `/predict` call, it runs a statistical drift test (KS-test) on the incoming feature against the reference distribution. If drift is detected, the service automatically fires a `repository_dispatch` event to GitHub, which triggers the CI/CD pipeline to retrain, rebuild, and redeploy the model — without any manual intervention.

### Architecture

```
HTTP Request  →  FastAPI /predict
                     │
                     ├── KSDrift (Alibi Detect) ── no drift ──► return prediction
                     │
                     └── drift=True
                              │
                              ├── Increment Prometheus counter (drift_detected_total)
                              ├── Log WARNING to stdout (collected by Loki)
                              └── POST /repos/.../dispatches (GitHub API)
                                           │
                                           ▼
                              GitHub Actions: MLOps Final Project CI/CD
                                  ├── python model/train.py
                                  ├── docker build & push  →  Docker Hub
                                  └── sed values.yaml tag → git commit & push
                                                                   │
                                                                   ▼
                                                      ArgoCD detects diff in Git
                                                      Rolling update in K8s cluster
```

### Tech Stack

| Layer | Tool |
|---|---|
| Inference API | FastAPI + Uvicorn |
| Drift Detection | Alibi Detect (`KSDrift`) |
| Containerization | Docker (`python:3.9-slim`) |
| Orchestration | Kubernetes |
| Deployment (GitOps) | ArgoCD |
| Helm Packaging | Helm 3 |
| CI/CD | GitHub Actions |
| Metrics | Prometheus (`prometheus_client`) + ServiceMonitor CRD |
| Dashboards | Grafana |
| Log Aggregation | Loki + Promtail |
| Image Registry | Docker Hub (`crossfil/aiops-quality-project`) |

### Project Structure

```
final-project/aiops-quality-project/
├── app/
│   ├── main.py              # FastAPI app: /predict, /metrics, drift logic, retrain trigger
│   └── requirements.txt
├── model/
│   ├── train.py             # Retrain script: increments version, saves model.pkl
│   └── model.pkl            # Serialized model (dict with version, coefficient)
├── helm/
│   ├── Chart.yaml
│   ├── values.yaml          # image.tag is auto-updated by CI on every retrain
│   └── templates/
│       ├── deployment.yaml  # K8s Deployment with resource limits and GitHub token secret
│       ├── service.yaml
│       └── servicemonitor.yaml  # Prometheus ServiceMonitor CRD
├── argocd/
│   ├── application.yaml     # ArgoCD app: syncs helm/ from this repo to cluster
│   └── prometheus-app.yaml  # ArgoCD app: deploys kube-prometheus-stack
├── prometheus/
│   └── prometheus-instance.yaml  # Prometheus CRD with wildcard selectors
├── grafana/
│   └── dashboards.json
└── Dockerfile
```

### CI/CD Pipeline (`.github/workflows/final-project.yml`)

Triggered by: `push` to `main`, `workflow_dispatch`, or `repository_dispatch` (type: `retrain_trigger`)

1. Checkout code with write token
2. Set up Python 3.9, install requirements
3. Run `model/train.py` — bumps version, randomises coefficient, saves `model.pkl`
4. Log in to Docker Hub
5. Build image tagged with `${{ github.sha }}`, push to `crossfil/aiops-quality-project`
6. `sed` replaces `tag:` in `helm/values.yaml` with the new SHA
7. Commits and pushes `values.yaml` back to the repo (`[skip ci]`)
8. ArgoCD picks up the diff and performs a rolling update in the cluster

### Key Design Decisions

- **`repository_dispatch` as the glue layer** — the running service directly triggers CI via the GitHub API, making retraining fully event-driven with no external orchestrator
- **Commit SHA as image tag** — every retrain produces a unique, traceable image; `latest` is also pushed for convenience
- **ArgoCD `selfHeal: true`** — cluster state is always reconciled to Git, preventing configuration drift
- **`ServiceMonitor` CRD** — metrics scraping is declared in code alongside the service, not in a separate Prometheus config file
- **GitHub token injected via Kubernetes `Secret`** — the service authenticates to the GitHub API at runtime without hardcoded credentials

### How to Run

```bash
# 1. Deploy Prometheus stack via ArgoCD
kubectl apply -f argocd/prometheus-app.yaml

# 2. Deploy the application via ArgoCD
kubectl apply -f argocd/application.yaml

# 3. Create GitHub token secret
kubectl create secret generic github-api-token --from-literal=token=YOUR_GITHUB_TOKEN

# 4. Forward port
kubectl port-forward svc/aiops-service-aiops 8000:80

# 5. Normal inference request
curl -X POST http://localhost:8000/predict \
     -H "Content-Type: application/json" \
     -d '{"feature_value": 2.5}'

# 6. Trigger drift (value far outside reference range [1.0, 5.0])
curl -X POST http://localhost:8000/predict \
     -H "Content-Type: application/json" \
     -d '{"feature_value": 999.0}'
# → drift: true, GitHub Actions retrain pipeline fires automatically
```

### Response Schema

```json
{
  "prediction": 1.75,
  "drift": false,
  "model_version": 1.2
}
```
