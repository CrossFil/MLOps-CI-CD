# FastAPI‑inference
import pickle
import numpy as np
from fastapi import FastAPI, Response  
from pydantic import BaseModel
import logging
from alibi_detect.cd import KSDrift

from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aiops-service")

app = FastAPI()

DRIFT_COUNTER = Counter('drift_detected_total', 'Total number of detected drift events')


class InputData(BaseModel):
    feature_value: float

model = None
drift_detector = None
reference_data = np.array([[1.0], [2.0], [3.0], [4.0], [5.0]])


@app.on_event("startup")
def load_resources():
    global model, drift_detector
    with open('model/model.pkl', 'rb') as f:
        model = pickle.load(f)
    drift_detector = KSDrift(reference_data, p_val=0.05)
    logger.info("Model and Drift Detector loaded")



@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/predict")
async def predict(data: InputData):
    x = np.array([[data.feature_value]])
    drift_result = drift_detector.predict(x)
    is_drift = int(drift_result['data']['is_drift'])

    if is_drift:
        logger.warning("!!! DRIFT DETECTED !!!")
        DRIFT_COUNTER.inc()

    prediction = data.feature_value * model.get("coefficient", 1.0)

    return {
        "prediction": prediction,
        "drift": bool(is_drift),
        "model_version": model.get("version")
    }
