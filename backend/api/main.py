# backend/api/main.py
from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .routes import lines as lines_routes
from .routes import status as status_routes
from .services.ingest import run_ingest_cycle
# from .routes import alerts as alerts_routes


# ---- Lifespan: startup/shutdown without deprecated decorators ----
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run one cycle so the UI isn't empty on the first boot
    try:
        run_ingest_cycle()
    except Exception as e:
        print("Initial ingest failed:", e)

    scheduler = BackgroundScheduler()
    scheduler.add_job(run_ingest_cycle, "interval", seconds=30, max_instances=1)
    scheduler.start()
    try:
        yield
    finally:
        if scheduler.running:
            scheduler.shutdown(wait=False)


app = FastAPI(title="NYC Transit Pulse", version="0.1.1", lifespan=lifespan)

# ---- Templates (server-rendered HTML) ----
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


# ---- Health ----
@app.get("/healthz")
def healthz():
    return {"status": "ok"}


# ---- HTML routes ----
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "NYC Transit Pulse"}
    )


# ---- API routes ----
app.include_router(status_routes.router, tags=["public"])
app.include_router(lines_routes.router, tags=["public"])
# app.include_router(alerts_routes.router, tags=["public"])
