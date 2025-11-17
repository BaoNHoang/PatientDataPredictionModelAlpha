import PatientDetailClient from "../../../components/patientDetailClient";

export default async function PatientDetailPage({ params }) {
  const { id } = await params; 

  const res = await fetch(`http://127.0.0.1:8000/patient/${id}`, {
    cache: "no-store",
  });

  const patient = await res.json();

  return <PatientDetailClient patient={patient} />;
}