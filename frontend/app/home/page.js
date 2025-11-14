"use client";
import Link from "next/link";
import { motion } from "framer-motion";
import { Stethoscope, Users, ActivitySquare } from "lucide-react";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-100 flex flex-col items-center px-6 py-16">
      
      {/* Welcome Text */}
      <motion.div
        className="text-center mb-16"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-6xl font-extrabold text-blue-700 tracking-tight">
          Welcome, Bao
        </h1>
        <p className="text-xl text-gray-700 mt-4">
          Your Medical Intelligence Dashboard
        </p>
      </motion.div>

      {/* Dashboard Cards */}
      <div className="grid md:grid-cols-3 gap-10 max-w-5xl w-full">
        
        {/* Predictor Card */}
        <motion.div
          whileHover={{ scale: 1.05 }}
          className="bg-white p-8 shadow-xl rounded-3xl border border-blue-200 hover:shadow-2xl transition cursor-pointer"
        >
          <Link href="/dashboard">
            <div className="flex flex-col items-center text-center">
              <Stethoscope className="w-16 h-16 text-blue-600 mb-4" />
              <h2 className="text-2xl font-bold text-gray-800">Patient Predictor</h2>
              <p className="text-gray-600 mt-2">
                Predict disease progression using patient biomarkers.
              </p>
            </div>
          </Link>
        </motion.div>

        {/* View Patients Card */}
        <motion.div
          whileHover={{ scale: 1.05 }}
          className="bg-white p-8 shadow-xl rounded-3xl border border-blue-200 hover:shadow-2xl transition cursor-pointer"
        >
          <Link href="/patients">
            <div className="flex flex-col items-center text-center">
              <Users className="w-16 h-16 text-green-600 mb-4" />
              <h2 className="text-2xl font-bold text-gray-800">View Patients</h2>
              <p className="text-gray-600 mt-2">
                Browse your entire patient list and profiles.
              </p>
            </div>
          </Link>
        </motion.div>

        {/* Add More Features Card */}
        <motion.div
          whileHover={{ scale: 1.05 }}
          className="bg-white p-8 shadow-xl rounded-3xl border border-blue-200 hover:shadow-2xl transition cursor-pointer"
        >
          <div className="flex flex-col items-center text-center opacity-60">
            <ActivitySquare className="w-16 h-16 text-purple-500 mb-4" />
            <h2 className="text-2xl font-bold text-gray-800">Analytics (Coming Soon)</h2>
            <p className="text-gray-600 mt-2">
              View overall trends and health analytics.
            </p>
          </div>
        </motion.div>

      </div>
    </div>
  );
}
