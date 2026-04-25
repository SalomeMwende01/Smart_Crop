# FieldPulse Monitoring System

FieldPulse is a role-based crop field monitoring platform built for the SmartSeason technical assessment.
It helps Admin Coordinators and Field Agents track field lifecycle, submit observations, and surface risk early.

## Stack
- Backend: Django + Django REST Framework + Token Authentication
- Frontend: React + Vite + React Router
- Database: MySQL (relational)

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

## Database Guide
This project is configured to use **MySQL by default**.

### Where data is stored
- With `DB_ENGINE=mysql`, data is stored inside MySQL server.

### MySQL environment variables
Set these in `.env` (copied from `.env.example`):
- `DB_ENGINE=mysql`
- `MYSQL_DATABASE=fieldpulse_db`
- `MYSQL_USER=root`
- `MYSQL_PASSWORD=...`
- `MYSQL_HOST=127.0.0.1`
- `MYSQL_PORT=3306`

### Create and inspect the MySQL database
Create DB once:
```sql
CREATE DATABASE fieldpulse_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Inspect DB/tables:
```bash
mysql -u root -p
```
```sql
SHOW DATABASES;
USE fieldpulse_db;
SHOW TABLES;
```

### Optional SQLite mode (creates a local file)
If you want a visible file database for quick local testing:
- set `DB_ENGINE=sqlite` in `.env`
- run `python backend/manage.py migrate`

Then Django will create `backend/db.sqlite3`.

## Local Setup
### 1. Clone and open project
```bash
git clone https://github.com/SalomeMwende01/Smart_Crop.git
cd Smart_Crop
```

### 2. Backend setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cp .env.example .env
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

## Assumptions
- Admin handles field creation and assignment.
- Agents do not directly edit field metadata; they submit updates.
- Risk thresholds are intentionally simple and can be tuned with agronomy input.
