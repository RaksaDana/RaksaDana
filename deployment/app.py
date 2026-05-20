from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import tensorflow as tf
import joblib
import math

app = FastAPI()

# Load model dan scaler
model = tf.keras.models.load_model("model.keras")
scaler = joblib.load("scaler.pkl")

class InputData(BaseModel):
    features: list  # shape (60, 15)
    current_close: float

@app.post("/predict")
def predict(data: InputData):
    # Convert ke numpy
    X = np.array(data.features)  # (60, 15)
    X_scaled = scaler.transform(X)  # scale fitur
    X_scaled = X_scaled.reshape(1, 60, 15)  # (1, 60, 15)

    # Prediksi log return
    log_return = model.predict(X_scaled)[0][0]

    # Rekonstruksi harga
    predicted_close = data.current_close * math.exp(log_return)

    return {
        "predicted_log_return": float(log_return),
        "predicted_close": float(predicted_close)
    }