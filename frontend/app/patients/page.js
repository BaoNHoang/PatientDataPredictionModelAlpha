"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";

export default function PatientsPage() {
  const [patients, setPatients] = useState([
    { name: "John Doe", age: 45, bmi: 24.5 },
    { name: "Jane Smith", age: 38, bmi: 27.1 },
    { name: "Alice Johnson", age: 52, bmi: 30.2 },
  ]);

  return (
    <div className="min-h-screen bg-gradient-to-tr from-purple-50 via-white to-blue-50 p-8 flex flex-col items-center">
      
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

      {/* Page Title */}
      <h1 className="text-4xl font-bold text-gray-700 mb-8 text-center">All Patients</h1>

      {/* Patient Cards */}
      <div className="grid md:grid-cols-3 gap-6 w-full max-w-5xl">
        {patients.map((p, i) => (
          <motion.div
            key={i}
            className="bg-white rounded-3xl p-6 shadow-md border border-gray-100 hover:shadow-xl transition-transform transform hover:-translate-y-1"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
          >
            <h2 className="text-2xl font-semibold mb-3 text-gray-800">{p.name}</h2>
            <p className="text-gray-700 mb-1"><b>Age:</b> {p.age}</p>
            <p className="text-gray-700"><b>BMI:</b> {p.bmi}</p>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
