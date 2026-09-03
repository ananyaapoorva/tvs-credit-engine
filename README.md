# 🏆 TVS Credit EPIC 8 Hackathon: Alternative Data Credit Engine

An AI-powered alternative credit scoring engine leveraging GST data, UPI transaction trends, telecom recharge patterns, utility bill payments, e-commerce activity, and mobility/vehicle usage patterns to generate explainable risk scores for first-time borrowers, gig workers, small merchants, and informal sector workers.

## 🚀 Key Features

*   **Multi-Source Alternative Data Integration:** Processes 6 disparate data sources (GST, UPI, Telecom, Utility, E-commerce, Mobility).
*   **Deterministic Rule-Based Scoring:** Transparent, explainable, and fully deterministic risk scoring logic mapped from 0-100.
*   **Explainable AI (XAI) Output:** Generates human-readable summaries and categorizes risk factors (positive/negative/neutral) dynamically.
*   **Dynamic Weighting:** Calculates overall risk based on a weighted average tailored for gig and informal sectors.
*   **Comprehensive API:** FastAPI backend with robust Pydantic validation and comprehensive endpoints.
*   **Responsive Dashboard:** React/Vite frontend with an interactive multi-step application form and animated visual gauges.

## 🏗️ Architecture

```mermaid
graph TD
    A[Client React App] -->|HTTP POST JSON| B(FastAPI Gateway)
    B --> C{Data Validator}
    C -->|Invalid| D[HTTP 422 Error]
    C -->|Valid| E[Scoring Engine]
    
    E --> F1[GST Scorer]
    E --> F2[UPI Scorer]
    E --> F3[Telecom Scorer]
    E --> F4[Utility Scorer]
    E --> F5[E-commerce Scorer]
    E --> F6[Mobility Scorer]
    
    F1 & F2 & F3 & F4 & F5 & F6 --> G[Weighted Aggregation]
    
    G --> H[Explainability Service]
    H --> I[SQLite Database]
    I --> J[Response Generator]
    J --> A
```

## 🛠️ Technology Stack

*   **Backend:** Python 3.11+, FastAPI, SQLAlchemy, Pydantic, Pytest (95% coverage)
*   **Frontend:** React 18, Vite, React Router, Custom CSS (No Tailwind)
*   **Infrastructure:** Docker, Docker Compose, GitHub Actions (CI/CD)

## 📦 Setup & Installation

### Option 1: Docker Compose (Recommended)

1.  Ensure you have Docker and Docker Compose installed.
2.  Clone the repository and run:
    ```bash
    docker-compose up --build
    ```
3.  Access the applications:
    *   **Frontend Dashboard:** `http://localhost:80`
    *   **Backend API Docs (Swagger):** `http://localhost:8000/docs`

### Option 2: Local Development Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 🧪 Testing

The backend includes a comprehensive test suite (82 tests) covering all scoring rules, business logic, and API endpoints.

```bash
cd backend
source venv/bin/activate
pytest tests/ -v --cov=app
```

## 📚 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/health` | System health check |
| `POST` | `/api/v1/credit/score` | Submit application & calculate score |
| `GET` | `/api/v1/credit/score/{id}` | Retrieve specific credit score by ID |
| `GET` | `/api/v1/credit/customer/{id}/scores` | Get all scores for a customer |
| `POST` | `/api/v1/credit/compare` | Compare two customers' scores |
| `GET` | `/api/v1/credit/mock-customers` | Fetch 10 diverse mock profiles for testing |

## ⚙️ Scoring Logic (Weighting)

*   **UPI Data:** 30%
*   **GST Data:** 25%
*   **Telecom Data:** 15%
*   **Utility Data:** 15%
*   **E-commerce Data:** 10%
*   **Mobility Data:** 5%

*(Weights adjust dynamically if certain data sources are missing).*
