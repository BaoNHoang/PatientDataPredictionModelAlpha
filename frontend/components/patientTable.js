// components/PatientTable.js
"use client";
export default function PatientTable({ patients }) {
  return (
    <div className="bg-white rounded-xl shadow p-4 overflow-auto">
      <table className="w-full table-auto">
        <thead>
          <tr className="text-left text-sm text-gray-900">
            <th className="p-2">ID</th>
            <th>Age</th>
            <th>BMI</th>
            <th>Cholesterol</th>
            <th>BP</th>
            <th>Glucose</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {patients.map((p) => (
            <tr key={p.patient_id} className="border-t text-gray-900">
              <td className="p-2 font-medium">#{p.patient_id}</td>
              <td className="p-2">{p.age}</td>
              <td className="p-2">{p.bmi}</td>
              <td className="p-2">{p.cholesterol}</td>
              <td className="p-2">{p.blood_pressure}</td>
              <td className="p-2">{p.glucose}</td>
              <td className="p-2">
                {/* <Link href={`/patients/${p.patient_id}`}>
                  <button className="px-3 py-1 bg-blue-600 text-white rounded-lg">Open</button>
                </Link> */}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
