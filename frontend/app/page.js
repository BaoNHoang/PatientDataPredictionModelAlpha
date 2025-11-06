"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import { ActivityLogIcon, HeartIcon, PersonIcon } from "@radix-ui/react-icons";
import { WindIcon, RefreshCw } from "lucide-react"; 

export default function Dashboard() {
  const [patient, setPatient] = useState({
    cholesterol: "",
    blood_pressure: "",
    age: "",
    glucose: "",
    bmi: "",
  });

  const [diseaseData, setDiseaseData] = useState([]);
  const [loading, setLoading] = useState(false);

  const diseaseIcons = {
    Healthy: <ActivityLogIcon className="w-5 h-5 text-green-500" />,
    Diabetes: <PersonIcon className="w-5 h-5 text-yellow-500" />,
    "Heart Disease": <HeartIcon className="w-5 h-5 text-red-500" />,
    "Lung Disease": <WindIcon className="w-5 h-5 text-blue-500" />,
  };

  // Handle input typing 
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setPatient((prev) => ({ ...prev, [name]: value }));
  };

  // Predict button click 
  const predictDisease = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          cholesterol: parseFloat(patient.cholesterol),
          blood_pressure: parseFloat(patient.blood_pressure),
          age: parseFloat(patient.age),
          glucose: parseFloat(patient.glucose),
          bmi: parseFloat(patient.bmi),
        }),
      });

      const result = await response.json();

      // Expected backend response
      const newPredictions = Object.entries(result.predictions || {}).map(
        ([year, label], idx) => ({
          year,
          risk: idx + 1,
          label,
        })
      );

      setDiseaseData(newPredictions);
    } catch (error) {
      console.error("Prediction failed:", error);
    } finally {
      setLoading(false);
    }
  };

  // Clear input fields 
  const handleClear = () => {
    setPatient({
      cholesterol: "",
      blood_pressure: "",
      age: "",
      glucose: "",
      bmi: "",
    });
    setDiseaseData([]);
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-800 flex flex-col items-center py-10 px-4">
      <motion.div
        className="max-w-5xl w-full bg-white shadow-xl rounded-2xl p-8 border"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold mb-4 text-center">
          Patient Disease Prediction Dashboard
        </h1>

        {/* Patient Input Form */}
        <div className="bg-gray-100 p-5 rounded-xl shadow-inner mb-8">
          <h2 className="text-xl font-semibold mb-3">Enter Patient Data</h2>
          <div className="grid md:grid-cols-3 gap-4">
            {["age", "cholesterol", "blood_pressure", "glucose", "bmi"].map(
              (field) => (
                <div key={field} className="flex flex-col">
                  <label className="text-sm font-medium capitalize mb-1">
                    {field.replace("_", " ")}
                  </label>
                  <input
                    type="number"
                    name={field}
                    value={patient[field]}
                    onChange={handleInputChange}
                    className="border rounded-lg p-2"
                    placeholder="Enter value"
                  />
                </div>
              )
            )}
          </div>

          <div className="flex gap-3 mt-4">
          <button
            onClick={predictDisease}
            disabled={loading}
            className={`flex items-center justify-center gap-2 ${
              loading
                ? "bg-blue-400 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700"
            } text-white px-4 py-2 rounded-lg shadow-md min-w-[120px]`}
          >
            {loading ? (
              <>
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{
                    repeat: Infinity,
                    duration: 1,
                    ease: "linear",
                  }}
                >
                  <RefreshCw className="w-4 h-4" />
                </motion.div>
                <span>Predicting...</span>
              </>
            ) : (
              "Predict"
            )}
          </button>
            <button
              onClick={handleClear}
              className="flex items-center gap-2 bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-2 rounded-lg shadow-md"
            >
              <RefreshCw className="w-4 h-4" /> Clear Fields
            </button>
          </div>
        </div>

        {/* Patient Info */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <div className="bg-gray-100 p-5 rounded-xl shadow-inner">
            <h2 className="text-xl font-semibold mb-3">Patient Info</h2>
            <ul className="space-y-1 text-sm">
              <li><b>Age:</b> {patient.age || ""}</li>
              <li><b>Cholesterol:</b> {patient.cholesterol || ""}</li>
              <li><b>Blood Pressure:</b> {patient.blood_pressure || ""}</li>
              <li><b>Glucose:</b> {patient.glucose || ""}</li>
              <li><b>BMI:</b> {patient.bmi || ""}</li>
            </ul>
          </div>

          <div className="bg-gray-100 p-5 rounded-xl shadow-inner">
            <h2 className="text-xl font-semibold mb-3">Predicted Diseases</h2>
            <div className="space-y-3">
              {diseaseData.length === 0 ? (
                <p className="text-gray-500">No predictions yet.</p>
              ) : (
                diseaseData.map((d, i) => (
                  <div
                    key={i}
                    className="flex items-center justify-between bg-white p-3 rounded-lg shadow-sm"
                  >
                    <div className="flex items-center gap-2">
                      {diseaseIcons[d.label] || (
                        <ActivityLogIcon className="w-5 h-5 text-gray-400" />
                      )}
                      <span className="font-medium">{d.label}</span>
                    </div>
                    <span className="text-gray-500">{d.year}</span>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
