import os
import pickle
import logging
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("ml-service")

MODEL_VERSION = os.getenv("MODEL_VERSION", "v1.0.0")
MODEL_PATH = os.getenv("MODEL_PATH", "model.pkl")

app = FastAPI(title="ML Service", version=MODEL_VERSION)

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

class PredictRequest(BaseModel):
    features: List[float]

class PredictResponse(BaseModel):
    prediction: float | int | str
    version: str

class HealthResponse(BaseModel):
    status: str
    version: str

@app.get("/")
def root():
    return {"status": "ok", "version": MODEL_VERSION}

@app.get("/health", response_model=HealthResponse)
def health():
    logger.info("health check")
    return {"status": "ok", "version": MODEL_VERSION}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    logger.info("predict features_len=%d", len(req.features))
    y_pred = model.predict([req.features])[0]
    if hasattr(y_pred, "item"):
        y_pred = y_pred.item()
    return {"prediction": y_pred, "version": MODEL_VERSION}
