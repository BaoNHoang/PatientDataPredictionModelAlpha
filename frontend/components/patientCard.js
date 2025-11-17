// components/PatientCard.js
"use client";
import { useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";

export default function PatientCard({ patient }) {
  const [open, setOpen] = useState(false);

  return (
    <motion.div layout className="bg-white rounded-3xl p-6 shadow-md border border-blue-50">
      <div className="flex items-start justify-between">
        <div>
          <h3 className="text-xl font-semibold text-blue-700">Patient #{patient.patient_id}</h3>
          <p className="text-gray-700"><b>Age:</b> {patient.age}</p>
          <p className="text-gray-700"><b>BMI:</b> {patient.bmi}</p>
        </div>

        <div className="flex flex-col items-end gap-2">
          <button onClick={()=>setOpen(o=>!o)} className="px-3 py-1 bg-gray-900 rounded-lg">
            {open ? "Close" : "Details"}
          </button>
          <Link href={`/patients/${patient.patient_id}`}>
            <button className="px-3 py-1 bg-blue-600 text-white rounded-lg">Open</button>
          </Link>
        </div>
      </div>

      {open && (
        <motion.div initial={{opacity:0}} animate={{opacity:1}} className="mt-4 border-t pt-4">
          <p className="text-gray-700"><b>Cholesterol:</b> {patient.cholesterol}</p>
          <p className="text-gray-700"><b>Blood Pressure:</b> {patient.blood_pressure}</p>
          <p className="text-gray-700"><b>Glucose:</b> {patient.glucose}</p>
        </motion.div>
      )}
    </motion.div>
  );
}
