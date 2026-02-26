from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd

app = FastAPI(title="User Dropoff Risk API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# load model
model = joblib.load("../models/dropoff_model.pkl")


@app.get("/")
def home():
    return {"message": "API is running"}


from pydantic import BaseModel

class UserInput(BaseModel):
    sessions: int
    time_spent: int

@app.post("/predict")
def predict_dropoff(user: UserInput):
    data = [[user.sessions, user.time_spent]]

    prediction = model.predict(data)[0]
    probability = model.predict_proba(data)[0][1]

    return {
        "dropoff_prediction": int(prediction),
        "dropoff_probability": float(round(probability, 3))
    }