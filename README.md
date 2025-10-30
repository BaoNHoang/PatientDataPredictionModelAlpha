# 🧠 Patient Disease Prediction System

A **machine learning project** that simulates and predicts disease progression in patients using a **custom-built Random Forest algorithm** — without relying on scikit-learn models.  

The system:
- Generates realistic patient medical records (cholesterol, blood pressure, glucose, BMI, etc.)
- Predicts which disease a patient might develop after **1, 2, 5, and 10 years**
- Allows you to **update patient data** and **re-evaluate predictions**
- Trains and reuses your **own Random Forest model**

---

## 🚀 Features
- 🩺 Generate large, realistic dummy datasets of patients  
- 🤖 Custom Decision Tree & Random Forest implementation (no external ML libraries)  
- 🕒 Predict diseases across multiple future years (1, 2, 5, 10)  
- 🔁 Update patient information dynamically  
- 💾 Save and reuse trained models to skip retraining  
- 📊 Evaluate model performance and accuracy  

---

## 📂 Project Structure
```
📦 patient-disease-predictor
├── data/
│ ├── patients.csv
│ ├── labels.csv
│
├── treeUtility/
│ ├── node.py
│ ├── decisionTree.py
│ ├── randomForest.py
│
├── utility/
│ ├── generatePatientData.py
│ ├── patientManagementSystem.py
│
├── main.py
├── requirements.txt
└── README.md
```
# 🧰 Tech Stack

- Python 3.9+

- NumPy

- Pandas

- Custom Random Forest & Decision Tree implementation

# 💡 Future Improvements

- Add time-series modeling for more accurate long-term predictions

- Include more features like family history, smoking status, and exercise level

- Integrate with a lightweight web UI 

- Add model persistence (save and load trained forests automatically)

# 🧑‍💻 Author

Bao Hoang
- 🎓 Computer Science Student @ Christopher Newport University
- 📍 Yorktown, VA

