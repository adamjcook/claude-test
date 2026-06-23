# UK Farm Grant Matcher

Inspired by Clarkson's Farm. Helps UK farmers find which government grants and schemes they may be eligible for based on their farm profile, with clear reasoning for each result.

## Architecture

- `backend/` — Python FastAPI service. Loads a curated, hand-written dataset of real UK farming grants (`app/data/grants_seed.json`), and evaluates a submitted farm profile against each grant using a declarative rules engine (`app/matching/`). No database — grants are static, profiles are not persisted.
- `frontend/` — React + TypeScript (Vite) single-page app. A form collects the farm profile; results are grouped into Matched / Partially Matched / Not Matched, each with an expandable "why" explanation per grant.

## Running locally

**Backend** (Python 3.11+):

```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

Run tests: `.venv/bin/pytest -v`

**Frontend** (Node 20+):

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:5173 (proxies `/api` requests to the backend on port 8000).

## Deploying (e.g. to view on a phone)

The `Dockerfile` builds the frontend and serves it from the FastAPI backend as a single service (FastAPI mounts `frontend/dist` once it exists, so there's only one URL and one process to deploy). `render.yaml` configures this as a Render.com web service (free tier):

1. Push this repo to GitHub (already done if you're reading this on the deployed branch).
2. On [render.com](https://render.com), sign in with GitHub, choose "New > Blueprint", and select this repo/branch. Render will detect `render.yaml` and build the `Dockerfile` automatically.
3. Once deployed, Render gives you a public `https://<service-name>.onrender.com` URL — open it on any device, including a phone.

The same `Dockerfile` works on other container platforms (Railway, Fly.io, etc.) if you'd rather use one of those instead.

## Out of scope (v1)

User accounts/auth, persistence of farm profiles or results, saved/tracked grant applications, deadline notifications, an admin UI for editing grant data, live scraping of GOV.UK/RPA, and devolved-nation (Scotland/Wales/Northern Ireland) scheme equivalents — non-England farms currently just receive a clear "not eligible, England-only scheme" result rather than being matched against an equivalent scheme.

## Data hygiene

Grant data in `backend/app/data/grants_seed.json` is hand-curated and includes a `last_verified_date` per grant. It should be reviewed periodically against GOV.UK, since application windows, rates and eligibility rules change.
