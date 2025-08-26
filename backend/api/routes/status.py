from fastapi import APIRouter, Query, HTTPException

from ..models.lines import is_valid_line, normalize_line
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
    line_norm = normalize_line(line)
    if not is_valid_line(line_norm):
        raise HTTPException(status_code=400, detail=f"Unknown line '{line}'. Try /lines for valid IDs.")
    return get_history(line=line_norm, limit=limit)

@router.get("/forecast", response_model=ForecastResponse)
def forecast(line: str, horizon_minutes: int = 15):
    line_norm = normalize_line(line)
    if not is_valid_line(line_norm):
        raise HTTPException(status_code=400, detail=f"Unknown line '{line}'. Try /lines for valid IDs.")

    # existing stub logic:
    statuses = {s["line"]: s["status"] for s in get_status_snapshot()}
    cur = statuses.get(line_norm, "GOOD")
    if cur == "DELAYS":
        prob = 0.75
    elif cur == "PLANNED":
        prob = 0.45
    else:
        prob = 0.12
    risk = "HIGH" if prob >= 0.6 else ("MED" if prob >= 0.3 else "LOW")
    return {"line": line_norm, "horizon_minutes": horizon_minutes, "prob_delay": prob, "risk": risk}
