"use client";
import Link from "next/link";
import { motion } from "framer-motion";

export default function HomePage() {
  return (
    <div className="relative flex flex-col items-center justify-center min-h-screen overflow-hidden bg-gradient-to-tr from-blue-100 via-white to-purple-100 px-4">

      {/* Background Effects */}
      <div className="absolute inset-0 opacity-30">
        <div className="w-full h-full bg-[linear-gradient(to_right,#87a8ff20_1px,transparent_1px),linear-gradient(to_bottom,#87a8ff20_1px,transparent_1px)] bg-[size:50px_50px] animate-[gridMove_12s_linear_infinite]"></div>
      </div>

      <div className="absolute top-20 left-10 w-72 h-72 bg-blue-300 rounded-full blur-3xl opacity-20 animate-pulse"></div>

      <div className="absolute bottom-20 right-10 w-80 h-80 bg-purple-300 rounded-full blur-3xl opacity-20 animate-pulse"></div>

      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        {[...Array(20)].map((_, i) => (
          <div
            key={i}
            className="absolute w-2 h-2 bg-blue-300 rounded-full opacity-40 animate-float"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDuration: `${6 + Math.random() * 6}s`,
              animationDelay: `${Math.random() * 4}s`,
            }}
          />
        ))}
      </div>

      {/* Main Title */}
      <motion.h1
        className="text-9xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-700 to-purple-700 mb-4 text-center z-10"
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        MedPredict
      </motion.h1>

      {/* Slogan */}
      <motion.p
        className="text-3xl md:text-2xl font-semibold text-gray-800 mb-6 text-center max-w-2xl z-10"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4, duration: 0.8 }}
      >
        Predict, Prevent, Empower{" "}
        <span className="text-xl md:text-lg">your healthcare decisions</span>
      </motion.p>

      {/* Start Button */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8, duration: 0.8 }}
        className="z-10"
      >
        <Link href="/home">
          <motion.button
            className="bg-blue-600 hover:bg-blue-700 text-white px-14 py-5 rounded-4xl shadow-xl font-extrabold text-4xl tracking-wide"
            whileHover={{ scale: 1.08 }}
            whileTap={{ scale: 0.96 }}
          >
            Start
          </motion.button>
        </Link>
      </motion.div>
    </div>
  );
}
