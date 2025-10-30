# main.py
import utility.patientManagementSystem as PMS
import utility.generatePatientData as GPD

if __name__ == "__main__":
    # Step 1: Generate new dummy patient data
    GPD.generate_data(num_patients=1000, output_dir="data", seed=5)

    file_path = "data/"
    patient_data = file_path + "patients.csv"
    label_data =  file_path +"labels.csv"
    # Step 2: Initialize system
    system = PMS.MainModule(patient_data, label_data)

    # Step 3: Evaluate on unseen data
    system.evaluate()

    # Step 4: Predict a few patients
    system.predict_patient(1)
    system.predict_patient(10)

    # # Step 5: Update a patient and retrain
    # new_data = [120, 110, 45, 90, 24.5]
    # system.update_patient(1, new_data)

    # Step 6: Predict a brand new patient (custom input)
    new_patient = [150.3, 109.42, 29, 115.43, 28.7]  # cholesterol, blood_pressure, age, glucose, bmi
    system.predict_new_patient(new_patient)
