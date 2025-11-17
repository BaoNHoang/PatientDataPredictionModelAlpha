"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowLeft, ChevronLeft, ChevronRight, List, Grid } from "lucide-react";
import PatientTable from "../../components/patientTable";
import PatientCard from "../../components/patientCard";

export default function PatientsPage() {
  const [patients, setPatients] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [q, setQ] = useState("");
  const [sortBy, setSortBy] = useState("patient_id");
  const [sortDir, setSortDir] = useState("asc");
  const [pageSize, setPageSize] = useState(30);
  const [loading, setLoading] = useState(false);
  const [viewTable, setViewTable] = useState(false);

  async function load(p = page) {
    setLoading(true);
    try {
      const params = new URLSearchParams({
        page: p,
        page_size: pageSize,
        sort_by: sortBy,
        sort_dir: sortDir,
      });
      if (q) params.set("q", q);
      const res = await fetch(`http://127.0.0.1:8000/patients?${params.toString()}`);
      const data = await res.json();
      setPatients(data.patients || []);
      setTotalPages(data.total_pages || 1);
    } catch (err) {
      console.error("fetch patients", err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(1); setPage(1); }, [q, sortBy, sortDir, pageSize]);

  useEffect(() => { load(page); }, [page]);

  return (
    <div className="min-h-screen p-8 bg-gradient-to-tr from-purple-100 via-white to-blue-100 flex flex-col items-center">
      <div className="w-full max-w-6xl mb-6 flex items-center justify-between">
        <Link href="/home">
          <motion.button className="flex items-center gap-2 bg-gray-200 hover:bg-gray-300 text-gray-700 px-4 py-2 rounded-xl shadow-md font-medium">
            <ArrowLeft className="w-4 h-4" /> Back
          </motion.button>
        </Link>

        <div className="flex items-center gap-3">
          <button
            onClick={() => setViewTable(false)}
            className={`p-2 rounded-lg ${!viewTable ? "bg-blue-500 text-white" : "bg-white shadow"}`}
            title=""
          >
            <Grid/>
          </button>
          <button
            onClick={() => setViewTable(true)}
            className={`p-2 rounded-lg ${viewTable ? "bg-blue-500 text-white" : "bg-white shadow"}`}
            title=""
          >
            <List/>
          </button>
        </div>
      </div>

      {/* Controls */}
      <div className="w-full max-w-6xl mb-6 flex flex-col md:flex-row gap-4 items-center">
        <div className="flex-1">
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Search by patient id, age, etc."
            className="w-full px-4 py-3 rounded-xl border text-gray-900 placeholder-gray-500 bg-white shadow-sm"
          />
        </div>

        <div className="flex gap-3 items-center">
          <select value={sortBy} onChange={(e)=>setSortBy(e.target.value)} className="px-3 py-2 rounded-xl border">
            <option value="patient_id">ID</option>
            <option value="age">Age</option>
            <option value="bmi">BMI</option>
            <option value="cholesterol">Cholesterol</option>
            <option value="blood_pressure">Blood Pressure</option>
          </select>

          <select value={sortDir} onChange={(e)=>setSortDir(e.target.value)} className="px-3 py-2 rounded-xl border">
            <option value="asc">Ascending</option>
            <option value="desc">Descending</option>
          </select>

          <select value={pageSize} onChange={(e)=>setPageSize(Number(e.target.value))} className="px-3 py-2 rounded-xl border">
            <option value={15}>15</option>
            <option value={30}>30</option>
            <option value={50}>50</option>
          </select>

          {/* <button onClick={() => load(1)} className="px-4 py-2 bg-blue-500 text-white rounded-xl">Apply</button> */}
        </div>
      </div>

      {/* Content */}
      <div className="w-full max-w-6xl">
        {loading && <p className="text-gray-600 mb-4">Loading...</p>}

        {!viewTable ? (
          <div className="grid md:grid-cols-3 gap-6">
            {patients.map((p) => (
              <PatientCard key={p.patient_id} patient={p} />
            ))}
          </div>
        ) : (
          <PatientTable patients={patients} />
        )}
      </div>

      {/* Pagination */}
      <div className="flex items-center gap-4 mt-8">
        <button onClick={() => setPage(prev=>Math.max(1, prev-1))} disabled={page===1} className="p-2 bg-blue-500 rounded-xl"><ChevronLeft/></button>
        <span>Page {page} / {totalPages}</span>
        <button onClick={() => setPage(prev=>Math.min(totalPages, prev+1))} disabled={page===totalPages} className="p-2 bg-blue-500 rounded-xl"><ChevronRight/></button>
      </div>
    </div>
  );
}
