# Deployment Guide

## Local Development

### Prerequisites
- Python 3.9+ (3.11 recommended)
- Node.js 20+ (24 recommended)
- Git

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.
Interactive docs at `http://localhost:8000/docs`.

### Frontend
```bash
cd frontend
npm install
npm run dev
```

The dashboard will be available at `http://localhost:5173`.

---

## Docker Deployment

### Prerequisites
- Docker Engine 20+
- Docker Compose v2+

### Build and Run
```bash
docker compose up --build
```

### Access
- **Frontend:** http://localhost:80
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### Stop
```bash
docker compose down
```

---

## Production Deployment Notes

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./tvs_credit.db` | Database connection string |
| `API_HOST` | `0.0.0.0` | API bind address |
| `API_PORT` | `8000` | API port |
| `CORS_ORIGINS` | `*` | Allowed CORS origins (comma-separated) |
| `VITE_API_URL` | `http://localhost:8000/api/v1` | Frontend API base URL |

### Database

The application uses SQLite for development. For production, swap the `DATABASE_URL` to a PostgreSQL connection string. The SQLAlchemy ORM ensures compatibility.

### Security Checklist

- [ ] Set specific `CORS_ORIGINS` (not wildcard)
- [ ] Use HTTPS with a reverse proxy (nginx/Caddy)
- [ ] Set `DATABASE_URL` to a persistent volume or managed database
- [ ] Remove debug/reload flags from uvicorn
- [ ] Set appropriate rate limits on the API

### Production Uvicorn Command

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```
