import random
from datetime import datetime, timedelta
from .cache import set_status_snapshot
from .storage import insert_events

LINES = ["A","C","E","F","G","J","L","M","N","Q","R","W","Z","1","2","3","4","5","6","7","S","SIR"]
STATUSES = ["GOOD", "DELAYS", "PLANNED"]

def _fake_status():
    # ~80% GOOD, 15% DELAYS, 5% PLANNED
    r = random.random()
    if r < 0.8: s = "GOOD"
    elif r < 0.95: s = "DELAYS"
    else: s = "PLANNED"
    sev = {"GOOD":0, "DELAYS":2, "PLANNED":1}[s]
    msg = None if s=="GOOD" else ("Signal issues near Bedford Ave" if s=="DELAYS" else "Planned track work")
    return s, sev, msg

def run_ingest_cycle():
    now = datetime.utcnow()
    statuses = []
    events = []

    for line in LINES:
        status, severity, message = _fake_status()
        statuses.append({
            "line": line,
            "status": status,
            "message": message,
            "updated_at": now.isoformat()
        })
        events.append({
            "source": "fake_mta_alerts",
            "line": line,
            "status": status,
            "severity": severity,
            "message": message,
            "started_at": now - timedelta(minutes=random.randint(0, 20))
        })

    # cache + persist
    set_status_snapshot(statuses)
    insert_events(events)
