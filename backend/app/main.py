"""
TVS Credit Alternative Data Credit Engine - FastAPI Application.

Main entry point for the backend API server.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.routers.credit_routes import router as credit_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler: initialize database on startup."""
    init_db()
    yield


app = FastAPI(
    title="TVS Credit Alternative Data Credit Engine",
    description=(
        "AI-powered alternative credit scoring engine leveraging GST data, "
        "UPI transaction trends, telecom recharge patterns, utility bill payments, "
        "e-commerce activity, and mobility/vehicle usage patterns to generate "
        "explainable risk scores for first-time borrowers, gig workers, "
        "small merchants, and informal sector workers."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(credit_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
    )
