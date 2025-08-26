# backend/api/routes/lines.py
from fastapi import APIRouter
from ..models.lines import VALID_LINES

router = APIRouter()

@router.get("/lines")
def list_lines():
    # Sorted for stable UI display
    return sorted(list(VALID_LINES))
