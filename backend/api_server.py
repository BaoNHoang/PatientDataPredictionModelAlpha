# api_server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utility.patientManagementSystem import MainModule
import csv

app = FastAPI()

# block to handle frontend requests 
origins = [
    "http://localhost:3000", 
    "http://127.0.0.1:3000",
]

# Enable frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     
    allow_credentials=True,
    allow_methods=["*"],        
    allow_headers=["*"],
)

system = MainModule("data/patients.csv", "data/labels.csv")

class PatientInput(BaseModel):
    cholesterol: float
    blood_pressure: float
    age: float
    glucose: float
    bmi: float

@app.post("/predict")
def predict_disease(patient: PatientInput):
    new_data = [patient.cholesterol, patient.blood_pressure, patient.age, patient.glucose, patient.bmi]

    disease_names = ["Healthy", "Diabetes", "Heart Disease", "Lung Disease"]
    predictions = {}

    for year, model in system.models.items():
        pred = model.predict([new_data])[0]
        predictions[year] = disease_names[pred]

    return {"predictions": predictions}

@app.get("/patients")
def get_all_patients():
    patients = []
    with open("data/patients.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            patients.append({
                "patient_id": row["patient_id"],
                "cholesterol": float(row["cholesterol"]),
                "blood_pressure": float(row["blood_pressure"]),
                "age": int(row["age"]),
                "glucose": float(row["glucose"]),
                "bmi": float(row["bmi"])
            })
    return {"patients": patients}