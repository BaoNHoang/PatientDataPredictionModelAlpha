# generatePatientData.py
import pandas as pd
import numpy as np
import os

# CREATE DATA (Sickness Results)
def generate_data(num_patients, output_dir, seed=None):
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

    rng = np.random.default_rng(seed)

    patient_ids = np.arange(1, num_patients + 1)

    age = rng.integers(20, 80, size=num_patients)
    cholesterol = rng.normal(loc=180 + (age-20)*0.5, scale=25, size=num_patients)
    cholesterol = np.clip(cholesterol, 120, 320)

    blood_pressure = rng.normal(loc=110 + (age-20)*0.6, scale=15, size=num_patients)
    blood_pressure = np.clip(blood_pressure, 90, 200)

    glucose = rng.normal(loc=95 + (age-20)*0.3, scale=20, size=num_patients)
    glucose = np.clip(glucose, 70, 300)

    bmi = rng.normal(loc=25 + (age-20)*0.05, scale=4, size=num_patients)
    bmi = np.clip(bmi, 16, 50)

    patients_df = pd.DataFrame({
        "patient_id": patient_ids,
        "cholesterol": cholesterol.round(2),
        "blood_pressure": blood_pressure.round(2),
        "age": age,
        "glucose": glucose.round(2),
        "bmi": bmi.round(2),
    })

    # CREATE LABELS (Sickness Results)
    def disease_risk(row):
        """
        Calculates a cardiovascular risk score based on common clinical metrics.
        Returns a risk score from 0 (low) to ~10 (high).
        """
        risk = 0

        # Age
        if row["age"] >= 65:
            risk += 3
        elif row["age"] >= 55:
            risk += 2
        elif row["age"] >= 45:
            risk += 1

        # Cholesterol (mg/dL)
        if row["cholesterol"] >= 240:
            risk += 3
        elif row["cholesterol"] >= 200:
            risk += 2
        elif row["cholesterol"] >= 180:
            risk += 1

        # Blood pressure (systolic)
        if row["blood_pressure"] >= 160:
            risk += 3
        elif row["blood_pressure"] >= 140:
            risk += 2
        elif row["blood_pressure"] >= 120:
            risk += 1

        # Glucose (mg/dL)
        if row["glucose"] >= 200:
            risk += 3
        elif row["glucose"] >= 140:
            risk += 2
        elif row["glucose"] >= 100:
            risk += 1

        # BMI
        if row["bmi"] >= 35:
            risk += 2
        elif row["bmi"] >= 30:
            risk += 1

        return risk


    risks = patients_df.apply(disease_risk, axis=1)

    # ASSIGN DISEASE 
    def assign_disease(risk, modifier=0):
        """
        Assigns a disease category based on risk score.
        
        Categories:
        0 - Healthy
        1 - Diabetes
        2 - Heart Disease
        3 - Lung Disease
        """
        prob = np.clip(risk + modifier + np.random.normal(0, 1), 0, 14)
        
        if prob < 4:
            return 0  # Healthy
        elif prob < 8:
            return 1  # Diabetes
        elif prob < 11:
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

    # SAVE TO FILES
    os.makedirs(output_dir, exist_ok=True)
    patients_path = os.path.join(output_dir, "patients.csv")
    labels_path = os.path.join(output_dir, "labels.csv")

    patients_df.to_csv(patients_path, index=False)
    labels_df.to_csv(labels_path, index=False)

    print(f"Created {patients_path} and {labels_path} with {num_patients} records.")

    return patients_df, labels_df
