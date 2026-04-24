# FieldPulse Monitoring System

A role-based field monitoring web application for tracking crop progress across multiple fields in one growing season.

This project is built as a monorepo:
- `backend/` Django + Django REST Framework API
- `frontend/` React app for Admin and Field Agent dashboards

## Why this design
- Clear separation of concerns (API vs UI)
- Role-based access control for Admin and Field Agent
- Computed status logic for decision support (`Active`, `At Risk`, `Completed`)

## Stepwise Build Plan (Commit-by-Commit)
1. Initialize repository, naming, and base structure
2. Scaffold Django backend and project settings
3. Implement authentication, roles, and user endpoints
4. Implement fields, updates, and computed status logic
5. Scaffold React frontend and API integration setup
6. Build authentication screens and protected routes
7. Build Admin dashboard and field management pages
8. Build Field Agent dashboard and update flow
9. Write tests, polish UI, and seed demo data
10. Deployment configs + final README updates

## Initial Scope from Assessment
- Roles: Admin (Coordinator), Field Agent
- Field management: create fields, assign agents
- Updates: stage updates + notes
- Lifecycle stages: `Planted`, `Growing`, `Ready`, `Harvested`
- Computed status: `Active`, `At Risk`, `Completed`
- Dashboards per role with totals and status breakdowns

## Getting Started (to be expanded)
Detailed backend/frontend setup and deployment steps are added in later commits.
