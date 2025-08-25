from fastapi import APIRouter, Query
from ..models.schemas import LineStatus, ForecastResponse
from ..services.cache import get_status_snapshot
from ..services.storage import get_history

router = APIRouter()

@router.get("/status", response_model=list[LineStatus])
def read_status():
    # If cache empty, returns []
    return get_status_snapshot()

@router.get("/history")
def read_history(line: str = Query(..., min_length=1), limit: int = 200):
    return get_history(line=line, limit=limit)

@router.get("/forecast", response_model=ForecastResponse)
def forecast(line: str, horizon_minutes: int = 15):
    # Stubbed forecast until model is trained
    # Map current status -> crude risk bucket to make UI useful now
    statuses = {s["line"]: s["status"] for s in get_status_snapshot()}
    cur = statuses.get(line, "GOOD")
    if cur == "DELAYS":
        prob = 0.75
    elif cur == "PLANNED":
        prob = 0.45
    else:
        prob = 0.12
    risk = "HIGH" if prob >= 0.6 else ("MED" if prob >= 0.3 else "LOW")
    return {"line": line, "horizon_minutes": horizon_minutes, "prob_delay": prob, "risk": risk}
