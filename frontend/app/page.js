"use client";
import Link from "next/link";
import { motion } from "framer-motion";

export default function HomePage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-tr from-blue-50 via-white to-purple-50 px-4">
      
      {/* Main Title */}
      <motion.h1
        className="text-9xl md:text-9x1 font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-700 to-purple-700 mb-4 text-center"
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        MedPredict
      </motion.h1>

      {/* Slogan */}
      <motion.p
        className="text-3xl md:text-1xl font-semibold text-gray-800 mb-12 text-center max-w-2xl"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
      >
        Predict, Prevent, Empower{" "}
        <span className="text-xl md:text-1xs">your healthcare decisions</span> 
      </motion.p>

      {/* Buttons */}
      <div className="flex flex-col md:flex-row gap-6">
        <Link href="/dashboard">
          <motion.button
            className="bg-blue-600 hover:bg-blue-700 text-white px-10 py-4 rounded-2xl shadow-xl font-semibold text-lg"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            Go to Dashboard
          </motion.button>
        </Link>

        <Link href="/patients">
          <motion.button
            className="bg-green-600 hover:bg-green-700 text-white px-10 py-4 rounded-2xl shadow-xl font-semibold text-lg"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            View Patients
          </motion.button>
        </Link>
      </div>
    </div>
  );
}
