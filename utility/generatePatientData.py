import pandas as pd
import numpy as np
import os

def generate_data(num_patients, output_dir, seed):
    """
    Generate realistic dummy patient data and disease progression labels.
    
    Args:
        num_patients (int): Number of patients to simulate (default=500)
        output_dir (str): Directory to save the CSV files (default=current folder)
        
    Output:
        Creates:
            - patients.csv
            - labels.csv
        Returns:
            (patients_df, labels_df)
    """

    np.random.seed(seed)  # Seed for reproducing data 

    # CREATE PATIENT FEATURES
    patient_ids = np.arange(1, num_patients + 1)

    cholesterol = np.random.normal(loc=200, scale=30, size=num_patients).clip(120, 280)
    blood_pressure = np.random.normal(loc=130, scale=20, size=num_patients).clip(100, 180)
    age = np.random.randint(20, 80, size=num_patients)
    glucose = np.random.normal(loc=100, scale=25, size=num_patients).clip(70, 200)
    bmi = np.random.normal(loc=26, scale=5, size=num_patients).clip(18, 40)

    patients_df = pd.DataFrame({
        "patient_id": patient_ids,
        "cholesterol": cholesterol.astype(int),
        "blood_pressure": blood_pressure.astype(int),
        "age": age,
        "glucose": glucose.astype(int),
        "bmi": bmi.round(1),
    })

    # CREATE LABELS (Sickness Results)
    def disease_risk(row):
        risk = 0
        if row["cholesterol"] > 240: risk += 2
        if row["blood_pressure"] > 150: risk += 2
        if row["glucose"] > 140: risk += 2
        if row["bmi"] > 30: risk += 1
        if row["age"] > 50: risk += 1
        return risk

    risks = patients_df.apply(disease_risk, axis=1)

    def assign_disease(risk, modifier=0):
        prob = np.clip(risk + modifier + np.random.normal(0, 1), 0, 10)
        if prob < 3:
            return 0  # Healthy
        elif prob < 5:
            return 1  # Diabetes
        elif prob < 7:
            return 2  # Heart Disease
        else:
            return 3  # Lung Disease

    labels_df = pd.DataFrame({
        "patient_id": patient_ids,
        "1-year": [assign_disease(r, 0) for r in risks],
        "2-year": [assign_disease(r, 1) for r in risks],
        "5-year": [assign_disease(r, 2) for r in risks],
        "10-year": [assign_disease(r, 3) for r in risks],
    })

    #  SAVE TO FILES
    os.makedirs(output_dir, exist_ok=True)
    patients_path = os.path.join(output_dir, "patients.csv")
    labels_path = os.path.join(output_dir, "labels.csv")

    patients_df.to_csv(patients_path, index=False)
    labels_df.to_csv(labels_path, index=False)

    print(f"Created {patients_path} and {labels_path} with {num_patients} records.")

    return patients_df, labels_df
