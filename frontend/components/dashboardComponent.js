// dashboardComponent.js
"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { ActivityLogIcon, HeartIcon, PersonIcon } from "@radix-ui/react-icons";
import { WindIcon, RefreshCw, ArrowLeft } from "lucide-react";

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
  const [canPredict, setCanPredict] = useState(false);

  const diseaseIcons = {
    Healthy: <ActivityLogIcon className="w-5 h-5 text-green-500" />,
    Diabetes: <PersonIcon className="w-5 h-5 text-yellow-500" />,
    "Heart Disease": <HeartIcon className="w-5 h-5 text-red-500" />,
    "Lung Disease": <WindIcon className="w-5 h-5 text-blue-500" />,
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setPatient((prev) => ({ ...prev, [name]: value }));
  };

  useEffect(() => {
    const allFilled = Object.values(patient).every((val) => val !== "");
    setCanPredict(allFilled);
  }, [patient]);

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
      const newPredictions = Object.entries(result.predictions || {}).map(
        ([year, label]) => ({ year, label })
      );
      setDiseaseData(newPredictions);
    } catch (error) {
      console.error("Prediction failed:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setPatient({ cholesterol: "", blood_pressure: "", age: "", glucose: "", bmi: "" });
    setDiseaseData([]);
  };

  return (
    <div className="min-h-screen bg-gradient-to-tr from-blue-50 via-white to-purple-50 flex flex-col items-center py-10 px-4">
      {/* Back Button */}
      <div className="w-full max-w-5xl mb-6">
        <Link href="/">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="flex items-center gap-2 bg-gray-200 hover:bg-gray-300 text-gray-700 px-4 py-2 rounded-xl shadow-md font-medium"
          >
            <ArrowLeft className="w-4 h-4" /> Back to Home
          </motion.button>
        </Link>
      </div>

      {/* Dashboard Card */}
      <motion.div
        className="max-w-5xl w-full bg-white shadow-2xl rounded-3xl p-8 border border-gray-100"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold mb-6 text-center text-gray-700">
          Patient Disease Prediction
        </h1>

        {/* Patient Input Form */}
        <div className="grid md:grid-cols-3 gap-5 mb-6">
          {["age", "cholesterol", "blood_pressure", "glucose", "bmi"].map((field) => (
            <div key={field} className="flex flex-col">
              <label className="text-sm font-medium text-gray-600 mb-1 capitalize">
                {field.replace("_", " ")}
              </label>
              <input
                type="number"
                name={field}
                value={patient[field]}
                onChange={handleInputChange}
                className="border rounded-2xl p-3 focus:ring-2 focus:ring-blue-400 outline-none text-gray-900 font-medium bg-white shadow-sm"
                placeholder="Enter value"
              />
            </div>
          ))}
        </div>

        <div className="flex gap-4 mb-8">
          <button
            onClick={predictDisease}
            disabled={!canPredict || loading}
            className={`flex items-center justify-center gap-2 px-6 py-3 rounded-2xl shadow-md font-semibold transition-colors duration-200
              ${!canPredict || loading
                ? "bg-gray-300 cursor-not-allowed text-gray-600"
                : "bg-blue-600 hover:bg-blue-700 text-white"
            }`}
          >
            {loading ? (
              <>
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
                >
                  <RefreshCw className="w-5 h-5" />
                </motion.div>
                Predicting...
              </>
            ) : (
              "Predict"
            )}
          </button>
          <button
            onClick={handleClear}
            className="flex items-center gap-2 bg-gray-200 hover:bg-gray-300 text-gray-700 px-6 py-3 rounded-2xl shadow-md font-semibold"
          >
            <RefreshCw className="w-5 h-5" /> Clear
          </button>
        </div>

        {/* Predictions */}
        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-gradient-to-tr from-white to-blue-50 p-6 rounded-2xl shadow-md border border-gray-100">
            <h3 className="text-xl font-semibold mb-4 text-gray-700">Patient Info</h3>
            <ul className="space-y-2 text-gray-900 font-medium">
              <li><b>Age:</b> {patient.age || "-"}</li>
              <li><b>Cholesterol:</b> {patient.cholesterol || "-"}</li>
              <li><b>Blood Pressure:</b> {patient.blood_pressure || "-"}</li>
              <li><b>Glucose:</b> {patient.glucose || "-"}</li>
              <li><b>BMI:</b> {patient.bmi || "-"}</li>
            </ul>
          </div>

          <div className="bg-gradient-to-tr from-white to-purple-50 p-6 rounded-2xl shadow-md border border-gray-100">
            <h3 className="text-xl font-semibold mb-4 text-gray-700">Predicted Diseases</h3>
            <div className="space-y-3">
              {diseaseData.length === 0 ? (
                <p className="text-gray-500">No predictions yet.</p>
              ) : (
                diseaseData.map((d, i) => (
                  <motion.div
                    key={i}
                    className="flex items-center justify-between bg-white p-3 rounded-xl shadow-sm hover:shadow-md transition"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.1 }}
                  >
                    <div className="flex items-center gap-3">
                      {diseaseIcons[d.label] || <ActivityLogIcon className="w-5 h-5 text-gray-400" />}
                      <span className="font-medium text-gray-900">{d.label}</span>
                    </div>
                    <span className="text-gray-700">{d.year}</span>
                  </motion.div>
                ))
              )}
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
