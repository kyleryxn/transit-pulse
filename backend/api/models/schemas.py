from pydantic import BaseModel
from datetime import datetime

class LineStatus(BaseModel):
    line: str
    status: str   # GOOD | DELAYS | PLANNED
    message: str | None = None
    updated_at: datetime

class ForecastResponse(BaseModel):
    line: str
    horizon_minutes: int
    prob_delay: float
    risk: str  # LOW | MED | HIGH
