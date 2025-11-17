"use client";
import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { ArrowLeft, ChevronLeft, ChevronRight } from "lucide-react";

export default function PatientsPage() {
  const [patients, setPatients] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  async function fetchPatients(pageNum) {
    const res = await fetch(`http://127.0.0.1:8000/patients?page=${pageNum}`);
    const data = await res.json();
    setPatients(data.patients);
    setTotalPages(data.total_pages);
  }

  useEffect(() => {
    fetchPatients(page);
  }, [page]);

  return (
    <div className="min-h-screen bg-gradient-to-tr from-purple-100 via-white to-blue-100 p-8 flex flex-col items-center">

      {/* Back Button */}
      <div className="w-full max-w-5xl mb-6">
        <Link href="/home">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="flex items-center gap-2 bg-gray-200 hover:bg-gray-300 text-gray-700 px-4 py-2 rounded-xl shadow-md font-medium"
          >
            <ArrowLeft className="w-4 h-4" /> Back to Home
          </motion.button>
        </Link>
      </div>

      {/* Title */}
      <h1 className="text-4xl font-bold text-gray-700 mb-8">All Patients</h1>

      {/* Patient Grid */}
      <div className="grid md:grid-cols-3 gap-6 w-full max-w-5xl">
        {patients.map((p, i) => (
          <motion.div
            key={i}
            className="bg-white rounded-3xl p-6 shadow-md border border-blue-100 hover:shadow-xl transition-transform transform hover:-translate-y-1"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <h2 className="text-2xl font-semibold text-blue-700 mb-3">
              Patient #{p.patient_id}
            </h2>
            <p className="text-gray-700"><b>Age:</b> {p.age}</p>
            <p className="text-gray-700"><b>BMI:</b> {p.bmi}</p>
            <p className="text-gray-700"><b>Cholesterol:</b> {p.cholesterol}</p>
            <p className="text-gray-700"><b>Blood Pressure:</b> {p.blood_pressure}</p>
            <p className="text-gray-700"><b>Glucose:</b> {p.glucose}</p>
          </motion.div>
        ))}
      </div>

      {/* Pagination */}
      <div className="flex items-center gap-4 mt-10">
        <button
          disabled={page === 1}
          onClick={() => setPage(page - 1)}
          className="px-4 py-2 bg-blue-200 hover:bg-blue-300 rounded-xl disabled:opacity-40"
        >
          <ChevronLeft />
        </button>

        <span className="text-gray-700 text-lg font-medium">
          Page {page} / {totalPages}
        </span>

        <button
          disabled={page === totalPages}
          onClick={() => setPage(page + 1)}
          className="px-4 py-2 bg-blue-200 hover:bg-blue-300 rounded-xl disabled:opacity-40"
        >
          <ChevronRight />
        </button>
      </div>
    </div>
  );
}
