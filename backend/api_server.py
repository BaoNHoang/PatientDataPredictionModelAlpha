# api_server.py 
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import csv
import math
import statistics

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     
    allow_credentials=True,
    allow_methods=["*"],        
    allow_headers=["*"],
)

CSV_PATH = "data/patients.csv"
CSV_FIELDS = ["patient_id","cholesterol","blood_pressure","age","glucose","bmi"]

def read_all_rows():
    """Read CSV and return list of dicts with typed values."""
    rows = []
    with open(CSV_PATH, "r", newline='') as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                rows.append({
                    "patient_id": r["patient_id"],
                    "cholesterol": float(r["cholesterol"]),
                    "blood_pressure": float(r["blood_pressure"]),
                    "age": int(float(r["age"])),
                    "glucose": float(r["glucose"]),
                    "bmi": float(r["bmi"]),
                })
            except Exception:
                # Skip malformed row
                continue
    return rows

@app.get("/patients")
def get_patients(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=500),
    q: Optional[str] = Query(None),             # free text search: patient_id or numeric search
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
    min_bmi: Optional[float] = None,
    max_bmi: Optional[float] = None,
    sort_by: Optional[str] = Query("patient_id"),
    sort_dir: Optional[str] = Query("asc"),
):
    rows = read_all_rows()

    # Filtering
    def passes(r):
        if min_age is not None and r["age"] < min_age: return False
        if max_age is not None and r["age"] > max_age: return False
        if min_bmi is not None and r["bmi"] < min_bmi: return False
        if max_bmi is not None and r["bmi"] > max_bmi: return False
        if q:
            ql = q.lower()
            # if q is numeric, allow numeric matching
            if ql.isdigit():
                if (str(r["patient_id"]).lower().find(ql) == -1 and
                    str(r["age"]).find(ql) == -1):
                    return False
            else:
                if ql not in str(r["patient_id"]).lower():
                    return False
        return True

    filtered = [r for r in rows if passes(r)]

    # Sorting
    if sort_by not in CSV_FIELDS:
        sort_by = "patient_id"
    reverse = (sort_dir.lower() == "desc")
    try:
        filtered.sort(key=lambda x: x.get(sort_by, 0), reverse=reverse)
    except Exception:
        pass

    total = len(filtered)
    total_pages = math.ceil(total / page_size) if page_size else 1
    start = (page - 1) * page_size
    end = start + page_size
    page_rows = filtered[start:end]

    return {
        "patients": page_rows,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }

@app.get("/patients/{patient_id}")
def get_patient(patient_id: str):
    rows = read_all_rows()
    for r in rows:
        if str(r["patient_id"]) == str(patient_id):
            return {"patient": r}
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/patients/stats")
def patients_stats():
    rows = read_all_rows()
    if not rows:
        return {"count": 0, "averages": {}, "histograms": {}}

    ages = [r["age"] for r in rows]
    bmis = [r["bmi"] for r in rows]
    chol = [r["cholesterol"] for r in rows]
    bp = [r["blood_pressure"] for r in rows]
    glucose = [r["glucose"] for r in rows]

    def hist(values, buckets=10):
        mn, mx = min(values), max(values)
        if mn == mx:
            return [{"min": mn, "max": mx, "count": len(values)}]
        step = (mx - mn) / buckets
        bins = []
        for b in range(buckets):
            lo = mn + b*step
            hi = lo + step
            count = sum(1 for v in values if (v >= lo and v < hi) or (b == buckets-1 and v == mx))
            bins.append({"min": lo, "max": hi, "count": count})
        return bins

    return {
        "count": len(rows),
        "averages": {
            "age": statistics.mean(ages),
            "bmi": statistics.mean(bmis),
            "cholesterol": statistics.mean(chol),
            "blood_pressure": statistics.mean(bp),
            "glucose": statistics.mean(glucose),
        },
        "histograms": {
            "age": hist(ages, buckets=10),
            "bmi": hist(bmis, buckets=10),
            "cholesterol": hist(chol, buckets=10),
        }
    }
