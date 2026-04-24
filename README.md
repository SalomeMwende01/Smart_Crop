# FieldPulse Monitoring System

FieldPulse is a role-based crop field monitoring platform built for the SmartSeason technical assessment.
It helps Admin Coordinators and Field Agents track field lifecycle, submit observations, and surface risk early.

## Stack
- Backend: Django + Django REST Framework + Token Authentication
- Frontend: React + Vite + React Router
- Database: SQLite (dev default, swappable to PostgreSQL in production)

## Core Features
- Role-based access (`ADMIN`, `AGENT`)
- Field management (create, assign, monitor stages)
- Field updates (agent notes + stage progression)
- Computed status for each field (`Active`, `At Risk`, `Completed`)
- Role-specific dashboards with totals and status breakdowns

## Field Status Logic
Computed status is derived from `current_stage` and `planting_date`:
- `Completed`: when stage is `HARVESTED`
- `At Risk`:
  - `PLANTED` for more than 14 days
  - `GROWING` for more than 45 days
  - `READY` for more than 20 days
- `Active`: all other non-harvested conditions

This keeps logic simple and transparent while still surfacing actionable risk signals.

## Monorepo Structure
- `backend/` Django project (`config`, `accounts`, `monitoring`)
- `frontend/` React app
- `docs/` supporting notes

## Local Setup
### 1. Clone and open project
```bash
git clone <your-repo-url>
cd Smart_Crop
```

### 2. Backend setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
python backend/manage.py migrate
python backend/manage.py seed_demo
python backend/manage.py runserver
```
Backend runs on `http://127.0.0.1:8000`.

### 3. Frontend setup
In a second terminal:
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on `http://localhost:5173`.

## Demo Credentials
- Admin Coordinator: `coordinator` / `Pass1234!`
- Field Agent 1: `agent_rose` / `Pass1234!`
- Field Agent 2: `agent_karim` / `Pass1234!`

## Useful API Endpoints
- `POST /api/auth/login/`
- `POST /api/auth/logout/`
- `GET /api/auth/me/`
- `GET /api/auth/agents/` (admin only)
- `GET/POST /api/monitoring/fields/`
- `PATCH /api/monitoring/fields/{id}/`
- `GET/POST /api/monitoring/fields/{id}/updates/`
- `GET /api/monitoring/dashboard/`

## Running Tests
```bash
source .venv/bin/activate
python backend/manage.py test accounts monitoring -v 2
```

## Deployment Guide
### Option A: Render (recommended for quick demo)
1. Push this repository to GitHub.
2. Create a new **Web Service** for backend:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt && python manage.py migrate && python manage.py seed_demo`
   - Start Command: `gunicorn config.wsgi:application`
3. Add environment variables:
   - `DJANGO_SECRET_KEY`
   - `DJANGO_DEBUG=False`
   - `DJANGO_ALLOWED_HOSTS=<backend-service-domain>`
   - `DJANGO_CORS_ALLOWED_ORIGINS=<frontend-domain>`
4. Deploy frontend (Vercel/Netlify/Render Static Site):
   - Root Directory: `frontend`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `dist`
   - Env: `VITE_API_BASE_URL=https://<backend-domain>/api`

## Assumptions
- Admin handles field creation and assignment.
- Agents do not directly edit field metadata; they submit updates.
- Risk thresholds are intentionally simple and can be tuned with agronomy input.
