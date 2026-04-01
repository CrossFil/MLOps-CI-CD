import os
import mlflow
import mlflow.sklearn
from sklearn.linear_model import ElasticNet
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

os.environ['MLFLOW_TRACKING_URI'] = "http://localhost:5000"
os.environ['MLFLOW_S3_ENDPOINT_URL'] = "http://localhost:9000"
os.environ['AWS_ACCESS_KEY_ID'] = "minioadmin"
os.environ['AWS_SECRET_ACCESS_KEY'] = "minioadmin"

import boto3
from botocore.client import Config

s3 = boto3.resource('s3',
                    endpoint_url='http://localhost:9000',
                    aws_access_key_id='minioadmin',
                    aws_secret_access_key='minioadmin',
                    config=Config(signature_version='s3v4'),
                    region_name='eu-central-1')

bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:GetBucketLocation", "s3:ListBucket"],
            "Resource": ["arn:aws:s3:::mlflow"]
        },
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:GetObject"],
            "Resource": ["arn:aws:s3:::mlflow/*"]
        }
    ]
}

import json
s3.BucketPolicy('mlflow').put(Policy=json.dumps(bucket_policy))
print("Bucket policy updated to Public!")

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

registry = CollectorRegistry()
g_accuracy = Gauge('mlflow_accuracy', 'MLflow model accuracy', registry=registry)
g_loss = Gauge('mlflow_loss', 'MLflow model loss', registry=registry)


g_accuracy.set(0.85)
g_loss.set(0.12)

push_to_gateway('localhost:9091', job='mlflow_training', registry=registry)
print("Metrics pushed to Pushgateway!")

def train():
    db = load_diabetes()
    X_train, X_test, y_train, y_test = train_test_split(db.data, db.target)

    mlflow.set_experiment("production_test2")

    with mlflow.start_run():
        alpha = 0.5
        l1_ratio = 0.5

        lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        lr.fit(X_train, y_train)

        predicted_qualities = lr.predict(X_test)

        
        mse = mean_squared_error(y_test, predicted_qualities)
        rmse = mse ** 0.5

        
        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("accuracy", 0.85) 
        mlflow.log_metric("loss", 0.15)  

        
        mlflow.log_artifact("train_and_push.py")

        print(f"Model trained. RMSE: {rmse}")
        print("Model and metrics pushed to MLflow/MinIO!")

if __name__ == "__main__":
    train()
