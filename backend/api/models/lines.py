# backend/api/models/lines.py
VALID_LINES: set[str] = {
    # Letters
    "A","B","C","D","E","F","G","J","L","M","N","Q","R","W","Z",
    # Numbers
    "1","2","3","4","5","6","7",
    # Shuttles
    "S",
    # Staten Island Railroad
    "SIR"
}

def normalize_line(s: str) -> str:
    return (s or "").strip().upper()

def is_valid_line(s: str) -> bool:
    return normalize_line(s) in VALID_LINES
