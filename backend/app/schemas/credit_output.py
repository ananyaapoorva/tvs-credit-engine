"""Pydantic schemas for credit score output responses."""

from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class ComponentScores(BaseModel):
    """Individual component scores breakdown."""
    gst_score: float = Field(description="GST data score (0-100)")
    upi_score: float = Field(description="UPI transaction score (0-100)")
    telecom_score: float = Field(description="Telecom recharge score (0-100)")
    utility_score: float = Field(description="Utility payment score (0-100)")
    ecommerce_score: float = Field(description="E-commerce activity score (0-100)")
    mobility_score: float = Field(description="Mobility/vehicle score (0-100)")


class ExplainabilityFactor(BaseModel):
    """Single explainability factor for the credit score."""
    category: str = Field(description="Data source category")
    signal: str = Field(description="What was detected")
    impact: str = Field(description="positive, negative, or neutral")
    contribution: str = Field(description="Points contribution")
    explanation: str = Field(description="Human-readable reasoning")


class ExplainabilityOutput(BaseModel):
    """Complete explainability breakdown."""
    factors: List[ExplainabilityFactor] = Field(description="List of contributing factors")
    summary: str = Field(description="Overall summary of risk assessment")
    recommendation: str = Field(description="Recommended action")


class CreditScoreOutput(BaseModel):
    """Complete credit score response."""
    score_id: str = Field(description="Unique score identifier")
    customer_id: str = Field(description="Customer identifier")
    overall_risk_score: float = Field(description="Overall risk score (0-100)")
    risk_category: str = Field(description="Risk classification: low, medium, high")
    component_scores: ComponentScores = Field(description="Individual component scores")
    confidence_level: float = Field(description="Confidence level (0-100)")
    explainability: ExplainabilityOutput = Field(description="Detailed risk factor explanations")
    generated_at: datetime = Field(description="Score generation timestamp")


class CreditScoreListItem(BaseModel):
    """Condensed score for list views."""
    score_id: str
    overall_risk_score: float
    risk_category: str
    confidence_level: float
    generated_at: datetime


class CustomerScoresResponse(BaseModel):
    """Response for listing all scores for a customer."""
    customer_id: str
    customer_name: str
    scores: List[CreditScoreListItem]
    total_count: int


class CompareResponse(BaseModel):
    """Side-by-side comparison of two customer scores."""
    customer_1: Optional[CreditScoreOutput] = None
    customer_2: Optional[CreditScoreOutput] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    version: str = "1.0.0"
    database: str = "connected"


class ErrorResponse(BaseModel):
    """Standard error response."""
    detail: str
    error_code: Optional[str] = None
