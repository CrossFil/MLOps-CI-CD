# FastAPI‑inference
import pickle
import numpy as np
import os
import httpx  
from fastapi import FastAPI, Response
from pydantic import BaseModel
import logging
from alibi_detect.cd import KSDrift
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aiops-service")

app = FastAPI()

# GitHub config
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") 
REPO_OWNER = "CrossFil"
REPO_NAME = "MLOps-CI-CD"
EVENT_TYPE = "retrain_trigger" 
DRIFT_COUNTER = Counter('drift_detected_total', 'Total number of detected drift events')

class InputData(BaseModel):
    feature_value: float

model = None
drift_detector = None
reference_data = np.array([[1.0], [2.0], [3.0], [4.0], [5.0]])

@app.on_event("startup")
def load_resources():
    global model, drift_detector
    try:
        with open('model/model.pkl', 'rb') as f:
            model = pickle.load(f)
        drift_detector = KSDrift(reference_data, p_val=0.05)
        logger.info("Model and Drift Detector loaded")
    except Exception as e:
        logger.error(f"Error loading resources: {e}")

async def trigger_retrain():
    """GitHub Action run function"""
    if not GITHUB_TOKEN:
        logger.error("GITHUB_TOKEN not set. Cannot trigger retrain.")
        return

    url = f"https://api.api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/dispatches"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    data = {"event_type": EVENT_TYPE}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=data)
            if response.status_code == 204:
                logger.info("Successfully triggered GitHub retrain workflow!")
            else:
                logger.error(f"Failed to trigger workflow: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"Error calling GitHub API: {e}")

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/predict")
async def predict(data: InputData):
    # logging for LOKI
    logger.info(f"Inference request: data={data.dict()}") 
    
    x = np.array([[data.feature_value]])
    drift_result = drift_detector.predict(x)
    is_drift = int(drift_result['data']['is_drift'])

    if is_drift:
        logger.warning("!!! DRIFT DETECTED !!!")
        DRIFT_COUNTER.inc()
        # TRIGGER: run retrain asynchronously
        await trigger_retrain()

    # Primitive prediction logic
    prediction = data.feature_value * model.get("coefficient", 1.0)

    return {
        "prediction": prediction,
        "drift": bool(is_drift),
        "model_version": model.get("version")
    }
