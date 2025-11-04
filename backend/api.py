# api.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from utility.patientManagementSystem import MainModule

app = FastAPI()

# Enable frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model system
system = MainModule("data/patients.csv", "data/labels.csv")

class PatientData(BaseModel):
    cholesterol: float
    blood_pressure: float
    age: int
    glucose: float
    bmi: float

@app.post("/predict")
def predict(data: PatientData):
    features = [data.cholesterol, data.blood_pressure, data.age, data.glucose, data.bmi]
    results = {}

    for year, model in system.models.items():
        pred = model.predict(np.array(features).reshape(1, -1))[0]
        results[year] = int(pred)

    return results
