# patientManagementSystem.py
import pandas as pd
import numpy as np
import joblib
import os
from treeUtility import randomForest

# PATIENT MANAGEMENT SYSTEM
class MainModule:
    """
    Patient Disease Prediction System using Random Forest.
    
    This module:
    - Loads patient data and disease progression labels
    - Splits data into training and testing sets
    - Trains separate Random Forest models for each time horizon (1, 2, 5, 10 years)
    - Predicts and updates patient data
    """

    def __init__(self, patient_csv, label_csv, model_dir="models"):
            self.patient_csv = patient_csv
            self.label_csv = label_csv
            self.model_dir = model_dir
            os.makedirs(self.model_dir, exist_ok=True)

            self.X, self.y_dict = self.load_data()
            self.X_train, self.X_test, self.y_train_dict, self.y_test_dict = self.split_all()

            self.models = {}
            for year in self.y_dict:
                model_path = os.path.join(self.model_dir, f"{year}_model.pkl")
                if os.path.exists(model_path):
                    print(f"Loading saved model for {year}...")
                    self.models[year] = joblib.load(model_path)
                else:
                    print(f"Training new model for {year}...")
                    model = randomForest.RandomForest(n_trees=600, max_depth=40, min_samples_split=3, criterion="gini")
                    model.fit(self.X_train, self.y_train_dict[year])
                    joblib.dump(model, model_path)
                    self.models[year] = model

    def load_data(self):
        """Load features and labels from CSVs."""
        patients_df = pd.read_csv(self.patient_csv)
        labels_df = pd.read_csv(self.label_csv)

        X = patients_df.drop(columns=["patient_id"]).to_numpy()
        y_dict = {col: labels_df[col].to_numpy() for col in labels_df.columns if col != "patient_id"}

        return X, y_dict
    
    def split_all(self, test_size=0.2, random_state=42):
        """Split features and all label sets into train/test subsets."""
        n = self.X.shape[0]
        idx = np.arange(n)
        np.random.seed(random_state)
        np.random.shuffle(idx)

        split = int(n * (1 - test_size))
        train_idx, test_idx = idx[:split], idx[split:]

        X_train, X_test = self.X[train_idx], self.X[test_idx]

        y_train_dict = {k: v[train_idx] for k, v in self.y_dict.items()}
        y_test_dict = {k: v[test_idx] for k, v in self.y_dict.items()}

        return X_train, X_test, y_train_dict, y_test_dict

    def evaluate(self):
        """Evaluate model accuracy on unseen test data."""

        print("\nModel Performance on Test Data:")
        for year, model in self.models.items():
            y_pred = model.predict(self.X_test)
            y_true = self.y_test_dict[year]
            acc = np.mean(y_pred == y_true)
            print(f"  {year}: {acc * 100:.2f}% accuracy")

    def predict_patient(self, patient_id):
        """Predict diseases for a single patient across all future years."""
        patients_df = pd.read_csv(self.patient_csv)

        if patient_id not in patients_df["patient_id"].values:
            print(f"Patient {patient_id} not found.")
            return

        patient_row = (patients_df.loc[patients_df["patient_id"] == patient_id].drop(columns=["patient_id"]).to_numpy())

        disease_names = ["Healthy", "Diabetes", "Heart Disease", "Lung Disease"]
        print(f"\nPredictions for Patient {patient_id}:")
        print(f"  Current features: {patient_row.tolist()[0]}")

        for year, model in self.models.items():
            pred = model.predict(patient_row)[0]
            print(f"  → {year}: {disease_names[pred]}")

    def update_patient(self, patient_id, new_features):
        """
        Update patient data and optionally retrain.
        
        Args:
            patient_id (int): Patient ID to update
            new_features (list): [cholesterol, blood_pressure, age, glucose, bmi]
        """
        patients_df = pd.read_csv(self.patient_csv)
        if patient_id not in patients_df["patient_id"].values:
            print(f"Patient {patient_id} not found.")
            return

        feature_cols = patients_df.columns[1:]
        patients_df.loc[patients_df["patient_id"] == patient_id, feature_cols] = new_features
        patients_df.to_csv(self.patient_csv, index=False)

        print(f"\nUpdated patient {patient_id} data in CSV.")
        print(f"   New features: {dict(zip(feature_cols, new_features))}")

        # Reload updated data and retrain (for demo purposes)
        self.X, self.y_dict = self.load_data()
        self.X_train, self.X_test, self.y_train_dict, self.y_test_dict = self.split_all()
        self.train_all()

    def predict_new_patient(self, new_features):
        """
        Predict diseases for a brand-new patient (not in the CSV).
        Args:
            new_features (list or array): [cholesterol, blood_pressure, age, glucose, bmi]
        """
        new_features = np.array(new_features).reshape(1, -1)
        disease_names = ["Healthy", "Diabetes", "Heart Disease", "Lung Disease"]
        results = {}

        print("\nPredictions for New Patient:")
        print(f"  Input features: {new_features.tolist()[0]}")

        for year, model in self.models.items():
            pred = model.predict(new_features)[0]
            print(f"  → {year}: {disease_names[pred]}")
            results[year] = disease_names[pred]
        return results

