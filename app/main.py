import os
import pickle
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

# Берём версию модели из переменной окружения,
# иначе по умолчанию v1.0.0
MODEL_VERSION = os.getenv("MODEL_VERSION", "v1.0.0")

app = FastAPI(title="ML Service", version=MODEL_VERSION)

# Загрузка модели при старте
MODEL_PATH = os.getenv("MODEL_PATH", "model.pkl")

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


@app.get("/health", response_model=HealthResponse)
def health():
    return {"status": "ok", "version": MODEL_VERSION}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    y_pred = model.predict([req.features])[0]

    if hasattr(y_pred, "item"):
        y_pred = y_pred.item()

    return {
        "prediction": y_pred,
        "version": MODEL_VERSION,
    }
