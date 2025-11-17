# api_server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utility.patientManagementSystem import MainModule
from fastapi import Query
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
def get_all_patients(page: int = 1, page_size: int = 50):
    rows = []
    with open("data/patients.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    total = len(rows)
    
    start = (page - 1) * page_size
    end = start + page_size

    # Slice rows
    page_rows = rows[start:end]

    # Convert values
    patients = []
    for r in page_rows:
        patients.append({
            "patient_id": r["patient_id"],
            "cholesterol": float(r["cholesterol"]),
            "blood_pressure": float(r["blood_pressure"]),
            "age": int(r["age"]),
            "glucose": float(r["glucose"]),
            "bmi": float(r["bmi"]),
        })

    return {
        "patients": patients,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }