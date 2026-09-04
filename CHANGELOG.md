# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-09-04

### Added
- Initial release: Alternative Data Credit Scoring Engine
- FastAPI backend with SQLAlchemy ORM and SQLite database
- React 18 frontend with Vite bundler and custom CSS design system
- Deterministic rule-based scoring engine processing 6 data sources:
  - GST filings (turnover, consistency, filing frequency)
  - UPI transactions (volume, frequency, duration, average size)
  - Telecom recharge (consistency, amount, history)
  - Utility payments (timeliness, bill amount, history)
  - E-commerce activity (purchase frequency, return rate, order value)
  - Mobility/Vehicle (ownership, fuel expense, tracking duration)
- Explainability service generating human-readable risk factor breakdowns
- Interactive multi-step application form with real-time validation
- Animated circular risk gauge with color-coded risk categories
- Radar chart visualization of component scores (Recharts)
- Side-by-side applicant comparison page with overlay radar charts
- Exportable credit reports (PDF via browser print dialog)
- 10 diverse mock customer profiles for demo testing
- Comprehensive test suite (83 tests, 100% pass rate)
- Docker containerization (backend + frontend + nginx)
- GitHub Actions CI/CD pipeline (backend tests, frontend build, Docker build)
- Full documentation (API, Algorithm, Deployment, Contributing)

### Architecture
- Backend: FastAPI + SQLAlchemy + Pydantic + pytest
- Frontend: React 18 + Vite + React Router + Recharts
- Infrastructure: Docker Compose + GitHub Actions
- Database: SQLite (development), PostgreSQL-ready (production)
