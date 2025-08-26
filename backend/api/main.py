from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

from .routes import lines as lines_routes
from .routes import status as status_routes
from .services.ingest import run_ingest_cycle

app = FastAPI(title="NYC Transit Pulse", version="0.1.0")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

app.include_router(status_routes.router, tags=["public"])
app.include_router(lines_routes.router, tags=["public"])

# Background ingest job
scheduler = BackgroundScheduler()
scheduler.add_job(run_ingest_cycle, "interval", seconds=30, max_instances=1)
scheduler.start()

# Run an initial cycle so UI isn't empty on the first boot
try:
    run_ingest_cycle()
except Exception as e:
    print("Initial ingest failed:", e)
