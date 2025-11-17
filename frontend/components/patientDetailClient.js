"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";

export default function PatientDetailClient({ patient }) {
  if (!patient) return <p>Loading...</p>;

  return (
    <div className="min-h-screen p-10 bg-gradient-to-tr from-blue-50 via-white to-purple-50">
      <Link href="/patients">
        <button className="flex items-center gap-2 bg-gray-200 hover:bg-gray-300 text-gray-700 px-4 py-2 rounded-xl shadow-md font-medium">
          <ArrowLeft className="w-4 h-4" /> Back
        </button>
      </Link>

      <h1 className="mt-6 text-4xl font-bold text-gray-700">
        Patient #{patient.patient_id}
      </h1>

      <div className="mt-6 bg-white p-6 rounded-2xl shadow-md">
        <p><b>Age:</b> {patient.age}</p>
        <p><b>BMI:</b> {patient.bmi}</p>
        <p><b>Cholesterol:</b> {patient.cholesterol}</p>
        <p><b>Blood Pressure:</b> {patient.blood_pressure}</p>
        <p><b>Glucose:</b> {patient.glucose}</p>
      </div>
    </div>
  );
}
