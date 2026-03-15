# FastAPI‑inference
import pickle
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
import logging
from alibi_detect.cd import KSDrift 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aiops-service")

app = FastAPI()

class InputData(BaseModel):
    feature_value: float

model = None
drift_detector = None
# reference data
reference_data = np.array([[1.0], [2.0], [3.0], [4.0], [5.0]])

@app.on_event("startup")
def load_resources():
    global model, drift_detector
    # 1. load model
    with open('model/model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    # 2. initializing the drift detector
    # p_val 0.05 means 95% confidence in the presence of drift
    drift_detector = KSDrift(reference_data, p_val=0.05)
    logger.info("Model and Drift Detector loaded")

@app.post("/predict")
async def predict(data: InputData):
    # conver the input value into the detector format
    x = np.array([[data.feature_value]])
    
    # drift check
    drift_result = drift_detector.predict(x)
    is_drift = int(drift_result['data']['is_drift'])
    
    if is_drift:
        logger.warning("!!! DRIFT DETECTED !!!")
        # Тут ми пізніше додамо виклик GitHub Actions
    
    prediction = data.feature_value * model.get("coefficient", 1.0)
    
    return {
        "prediction": prediction,
        "drift": bool(is_drift),
        "model_version": model.get("version")
    }
