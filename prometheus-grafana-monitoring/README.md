# MLOps Experiment Tracking System

This project implements a GitOps-based ML infrastructure using Kubernetes, ArgoCD, MLflow, and Prometheus/Grafana.

## 1. How to run train_and_push.py
Before running the script, ensure you have the required libraries installed:

Bash 

`pip install -r experiments/requirements.txt`

To execute the training and push metrics/artifacts:

Ensure your local environment has access to the cluster services (see Port-Forwarding below).

Run the script from the project root:

Bash

`python experiments/train_and_push.py`

The script trains an ElasticNet model, logs parameters/artifacts to MLflow (S3/Postgres), and pushes accuracy/loss metrics to Prometheus via Pushgateway.

## 2. Verify MLflow and Pushgateway in the Cluster
Check the status of the pods and services in their respective namespaces:

Check Pods:

Bash

`
kubectl get pods -n mlflow
kubectl get pods -n monitoring`


You should see mlflow, postgres, minio, and pushgateway in a Running state.

Check Services:

Bash

`kubectl get svc -n mlflow
kubectl get svc -n monitoring`


## 3. How to Setup Port-Forwarding
To access the internal cluster services from your local machine, run the following commands in separate terminal windows:

ArgoCD UI:

https://localhost:8080/

<img width="1356" height="763" alt="Снимок экрана 2026-03-08 в 15 17 26" src="https://github.com/user-attachments/assets/5d263335-6177-4eba-8b42-9a23019eb067" />


MLflow UI:

Bash

`kubectl port-forward svc/mlflow -n mlflow 5000:5000
MinIO UI:`

<img width="1335" height="758" alt="Снимок экрана 2026-03-08 в 14 01 54" src="https://github.com/user-attachments/assets/b3368ba7-f1d6-4017-ad98-c489ce7d1333" />


<img width="1335" height="758" alt="Снимок экрана 2026-03-08 в 13 57 02" src="https://github.com/user-attachments/assets/8b59e2cc-45d6-49db-b9e1-10f8b5944537" />

Bash

`kubectl port-forward svc/minio -n mlflow 9001:9001`

<img width="1335" height="758" alt="Снимок экрана 2026-03-08 в 12 50 02" src="https://github.com/user-attachments/assets/533081cf-ec78-4a72-a7da-5541af24647e" />

<img width="1282" height="763" alt="Снимок экрана 2026-03-08 в 15 18 57" src="https://github.com/user-attachments/assets/97694717-bb1e-4051-9e15-4c03c53a90a0" />


Pushgateway:

Bash

`kubectl port-forward svc/pushgateway -n monitoring 9091:9091`

<img width="1335" height="758" alt="Снимок экрана 2026-03-08 в 14 49 43" src="https://github.com/user-attachments/assets/a5e4d1d3-9b61-44f2-8185-ad6f5922cbe7" />


Grafana:

Bash

`kubectl port-forward svc/grafana -n monitoring 3000:3000`

<img width="1220" height="640" alt="Снимок экрана 2026-03-08 в 15 07 16" src="https://github.com/user-attachments/assets/983d39bd-dace-4b02-a4ef-15b005cd2501" />

## 4. How to View Metrics in Grafana
Open your browser and go to http://localhost:3000.

Navigate to the Explore tab (compass icon on the left sidebar).

Select Prometheus as the Data Source.

In the query field, type the following metrics to see the graphs:

mlflow_accuracy

mlflow_loss

Click Run Query.

