import utility.patientManagementSystem as PMS
import utility.generatePatientData as GPD 

if __name__ == "__main__":

    patients, labels = GPD.generate_data(num_patients=100, output_dir="data", seed=1)

    print(patients.head(10))
    print(labels.head(10))

    system = PMS.MainModule("./data/patients.csv", "./data/labels.csv")

    system.predict_patient(1)

    system.predict_patient(2)

    new_data = [300, 175, 25, 500, 1]
    system.update_patient(1, new_data)

    system.predict_patient(1)