# NYC Transit Pulse

A real-time dashboard for NYC transit using **FastAPI**, **PostgreSQL**, **Redis**, and **Dash**.  
It ingests **MTA GTFS-realtime Alerts** and normalizes them into a modern alerts-first view (no more legacy status box).

## Features
- **Live Alerts**: Ingests GTFS-rt alerts every 30 seconds
- **Alerts API**:
  - `GET /alerts` — normalized active alerts (title, description, start/end, severity)
  - `GET /lines/health` — per-line rollup (no_alerts | planned | service_change | disrupted)
- **Legacy Status API** (backward-compatible):
  - `GET /status` — condensed GOOD/PLANNED/DELAYS snapshot
  - `GET /history` — recent event rows per line
- **Forecast API** (stub for now):
  - `GET /forecast?line=L&horizon=15m` — risk of delay in next 15 minutes
- **Dash UI**:
  - Displays alert cards (line, category, severity, message, timing)
  - Auto-refreshes every 30s

## Tech Stack
- **Backend**: Python, FastAPI, APScheduler (for ingest jobs)
- **Data**: PostgreSQL (historical), Redis (live cache)
- **Ingestion**: gtfs-realtime-bindings + httpx
- **Frontend**: Dash (Plotly)
- **Infra**: Docker + docker-compose, healthchecks
- **Testing**: pytest (basic endpoint checks)

## Directory Layout
```
nyc-transit-pulse/
  api/              # FastAPI app
    ml/             # model training & serving (future)
    models/         # pydantic schemas
    routes/         # /status, /alerts, /forecast
    services/       # ingest, cache, storage
    main.py
  web/              # Dash app
    app.py          # Dash frontend
  etl/              # SQL migrations
  infra/            # docker-compose.yml, Dockerfiles, .env
  tests/            # pytest tests
  CHANGELOG.md      
  README.md
  TODO.md
```

## Environment

Create a `.env` file in `infra/`:

```yml
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=transit
POSTGRES_USER=transit
POSTGRES_PASSWORD=transit

REDIS_URL=redis://redis:6379/0
API_BASE_URL=http://api:8000

# optional override
MTA_ALERTS_URL=https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys/all-alerts
```

> Keep a `.env.example` in version control, but `.env` should be git-ignored.


## Run locally

```powershell
cd infra
docker compose down -v        # stop and clear volumes
docker compose build --no-cache
docker compose up
```
```
- API: http://localhost:8000/docs  
- UI: http://localhost:8050  
```

## Example Usage

### Alerts

```powershell
curl http://localhost:8000/alerts | jq .
```


### Line Health

```powershell
curl http://localhost:8000/lines/health
```

## Development

### Run tests

```powershell
pytest tests
```

### Database inspection

```powershell
docker compose exec postgres psql -U transit -d transit -c "select * from alerts limit 10;"
```

## Roadmap

- [x] Create an MVP with fake data
- [ ] Add subway Trip Updates feeds (ETA predictions)
- [ ] Enrich alerts with weather / CitiBike data
- [ ] Train ML model to power /forecast
- [ ] Migrate Dash → React + Mapbox for richer maps
- [ ] Deploy to the cloud (Render, Fly.io, or AWS)

## License

GPL-3.0
