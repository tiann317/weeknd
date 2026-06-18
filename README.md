# Weeknd

A weekend hike finder for Germany and the Alps. Browse curated hikes on a map, find ones near
your location, and (planned) check which are reachable by train on the Deutschlandticket and what
the weather will be.

This is a work in progress. The map, hike browsing, and "nearby" search work end to end. Train
and weather integration exist as standalone scripts and are not yet wired into the API.

## Stack

- **Backend**: FastAPI, SQLAlchemy 2.0, Alembic, PostgreSQL 16 (`cube` + `earthdistance`
  extensions for geo radius queries), JWT auth (Argon2 password hashing).
- **Frontend**: Angular 21, Leaflet (OpenStreetMap tiles), Tailwind 4.
- **Infra**: Docker Compose, nginx reverse proxy + TLS, GitHub Actions → GHCR images →
  Watchtower auto-pull on the VPS.

## What works so far

- `GET /hikes` — list hikes, optional `?region=` filter.
- `GET /hikes/nearby?lat=&lon=&radius_km=` — radius search via Postgres `earthdistance`.
- `GET /hikes/{id}` — hike detail with start/end station info.
- Auth scaffolding: `/login/access-token`, `/users` (JWT, superuser-gated).
- Seed data: a handful of Alpine hikes + stations, including Deutschlandticket validity flags.

## Not yet wired in

- `backend/utils/utils.py` (DB train connections) and `backend/utils/weather.py` (Bright Sky)
  are exploratory CLI scripts. They are not imported by the API and reference config values that
  are not yet defined in `core/config.py`.

## Data model

- **Hike** — title, sport type, distance/duration/ascent, difficulty, start/end coords, GeoJSON
  geometry, region, optional start/end station FKs, source/attribution.
- **Station** — name, coords, DB EVA id, operator, `is_private_railway`, `dticket_valid`.
- **User** — email/username, Argon2 hash, active/superuser flags.

## Running locally

Requires Docker and Docker Compose.

```bash
cp backend/.env.example backend/.env   # fill in values; generate SECRET_KEY with: openssl rand -hex 32
docker compose up --build
```

The base compose plus `docker-compose.override.yaml` exposes:

- Frontend: http://localhost:4200
- Backend: http://localhost:8000 (Swagger at `/docs`)
- Postgres: localhost:5433

The backend container runs `alembic upgrade head` on start. To seed test data:

```bash
docker compose exec backend python seed.py
```

`DB_CLIENT_ID` / `DB_API_KEY` (DB API Marketplace) are only needed for the train scripts and can
be left as placeholders for the core app.

### Backend without Docker

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
# point POSTGRES_* at a running Postgres (with cube + earthdistance extensions)
cd backend && alembic upgrade head && python seed.py
uvicorn main:app --reload
```

## Deployment

Push to `main` triggers GitHub Actions, which builds and pushes
`ghcr.io/tiann317/weeknd-backend` and `-frontend`. Watchtower on the VPS polls GHCR and
redeploys. Production adds `docker-compose.prod.yaml` (nginx + Let's Encrypt + Watchtower).

## Tests / lint

```bash
ruff check backend/
cd frontend && npm test
```
