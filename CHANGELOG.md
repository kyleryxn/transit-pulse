# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2025-08-25

### Added

- Lifespan event handler using FastAPI’s `lifespan` context manager to replace deprecated `@app.on_event`
- Jinja2 template support:
  - Configured `Jinja2Templates` pointing to `backend/api/templates/`
  - Added a root `"/"` route that renders `index.html`
- New HTML entrypoint to serve a server-rendered landing page

### Changed

- Replaced old `@app.on_event("startup"/"shutdown")` hooks with `lifespan` contenxt to manage APScheduler background 
job lifecycle
- Migrations now include an additional `alerts.sql` file automatically during startup
- `main.py` structure updated: routers + templates + lifespan integrated for cleaner separation of API routes and HTML 
views
- Replaced the text box with a dropdown menu for selecting subway line

## [0.1.0] - 2025-08-25

- Initial release