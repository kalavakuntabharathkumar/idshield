from fastapi import FastAPI
from pydantic import BaseModel
from .policy import evaluate_policy
from .identity import sample_identities

app = FastAPI(title="Cloud Identity Data Protection Reporting API", version="1.0.0")

class ReportRequest(BaseModel):
    policy: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/identities")
def identities():
    return {"items": sample_identities()}

@app.post("/reports")
def report(request: ReportRequest):
    identities = sample_identities()
    results = [evaluate_policy(request.policy, item) for item in identities]
    return {"total": len(results), "passed": sum(r["passed"] for r in results), "results": results}
