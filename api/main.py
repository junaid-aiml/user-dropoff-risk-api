from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import joblib
import pandas as pd
import os


class CustomerData(BaseModel):
    tenure: int
    MonthlyCharges: float
    TotalCharges: float
    SeniorCitizen: int
    Partner: str
    Dependents: str
    PhoneService: str
    PaperlessBilling: str


app = FastAPI(title="User Dropoff Risk API")

# Load model once when API starts


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
model_path = os.path.join(BASE_DIR, "models", "logreg_churn_v1.pkl")

model = joblib.load(model_path)

@app.get("/")
def home():
    return {"message": "User Dropoff Risk API is running"}

@app.post("/predict")
def predict(data: CustomerData):
    df = pd.DataFrame([data.dict()])

    # ✅ apply same encoding as training
    df_encoded = pd.get_dummies(df)

    # ✅ align columns with model
    model_features = model.feature_names_in_
    df_encoded = df_encoded.reindex(columns=model_features, fill_value=0)

    prediction = model.predict(df_encoded)[0]
    probability = model.predict_proba(df_encoded)[0][1]

    return {
        "churn_prediction": int(prediction),
        "churn_probability": float(probability)
    }

    return {
        "churn_prediction": int(prediction),
        "churn_probability": float(probability)
    }