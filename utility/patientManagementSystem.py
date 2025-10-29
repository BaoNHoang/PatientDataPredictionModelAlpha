import pandas as pd
from treeUtility import randomForest

# PATIENT MANAGEMENT SYSTEM
class MainModule:
    """
    Patient disease prediction system.

    - Holds patient feature data (e.g. cholesterol, BP, etc.)
    - Trains separate Random Forests for multiple future horizons (1, 2, 5, 10 years)
    - Can update individual patient data and re-predict outcomes
    """
    def __init__(self, patient_csv, label_csv):
        self.patient_csv = patient_csv
        self.label_csv = label_csv
        self.X, self.y_dict = self.load_data()
        self.models = {year: randomForest.RandomForest(n_trees=20, max_depth=10) for year in self.y_dict}
        self.train_all()

    def load_data(self):
        """Load features and labels from CSVs."""
        patients_df = pd.read_csv(self.patient_csv)
        labels_df = pd.read_csv(self.label_csv)
        X = patients_df.drop(columns=["patient_id"]).to_numpy()
        y_dict = {col: labels_df[col].to_numpy() for col in labels_df.columns if col != "patient_id"}
        return X, y_dict

    def train_all(self):
        for year, model in self.models.items():
            model.fit(self.X, self.y_dict[year])

    def update_patient(self, patient_id, new_features):
        """Update patient’s feature row in the CSV and memory."""
        patients_df = pd.read_csv(self.patient_csv)
        patients_df.loc[patients_df["patient_id"] == patient_id, patients_df.columns[1:]] = new_features
        patients_df.to_csv(self.patient_csv, index=False)
        print(f"\nPatient {patient_id} data updated in CSV.")
        self.X, self.y_dict = self.load_data()

    def predict_patient(self, patient_id):
        """Predict future disease outcomes for a patient."""
        patients_df = pd.read_csv(self.patient_csv)
        patient_row = patients_df.loc[patients_df["patient_id"] == patient_id].drop(columns=["patient_id"]).to_numpy()
        disease_names = ["Healthy", "Diabetes", "Heart Disease", "Lung Disease"]
        print(f"\nPredictions for Patient {patient_id}: {patient_row.tolist()[0]}")
        for year, model in self.models.items():
            pred = model.predict(patient_row)[0]
            print(f"  → {year}: {disease_names[pred]}")
