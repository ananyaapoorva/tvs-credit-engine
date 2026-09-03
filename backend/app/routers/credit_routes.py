from typing import Optional, List, Dict
"""
Credit scoring API routes.

Provides endpoints for submitting credit applications, retrieving scores,
comparing customers, and health checks.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.credit_score import CreditScore
from app.models.customer import Customer
from app.schemas.credit_input import CreditApplicationInput
from app.schemas.credit_output import (
    CompareResponse,
    ComponentScores,
    CreditScoreListItem,
    CreditScoreOutput,
    CustomerListItem,
    CustomerScoresResponse,
    ExplainabilityFactor,
    ExplainabilityOutput,
    HealthResponse,
)
from app.services.data_validator import validate_application_data
from app.services.explainability import generate_explanation
from app.services.scoring_engine import calculate_credit_score
from app.utils.mock_data import get_all_mock_customers, get_mock_customer

router = APIRouter(prefix="/api/v1", tags=["credit"])


def _build_score_output(score_record: CreditScore) -> CreditScoreOutput:
    """Build a CreditScoreOutput from a database record."""
    explanation = score_record.explanation or {"factors": [], "summary": "", "recommendation": ""}
    return CreditScoreOutput(
        score_id=score_record.score_id,
        customer_id=score_record.customer_id,
        overall_risk_score=score_record.overall_risk_score,
        risk_category=score_record.risk_category,
        component_scores=ComponentScores(
            gst_score=score_record.gst_score,
            upi_score=score_record.upi_score,
            telecom_score=score_record.telecom_score,
            utility_score=score_record.utility_score,
            ecommerce_score=score_record.ecommerce_score,
            mobility_score=score_record.mobility_score,
        ),
        confidence_level=score_record.confidence_level,
        explainability=ExplainabilityOutput(
            factors=[ExplainabilityFactor(**f) for f in explanation.get("factors", [])],
            summary=explanation.get("summary", ""),
            recommendation=explanation.get("recommendation", ""),
        ),
        generated_at=score_record.generated_at,
    )


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for deployment testing."""
    return HealthResponse(status="healthy", version="1.0.0", database="connected")


@router.post("/credit/score", response_model=CreditScoreOutput)
async def create_credit_score(
    application: CreditApplicationInput,
    db: Session = Depends(get_db),
):
    """
    Submit a credit application and receive a risk score.

    Validates input, calculates component scores for all 6 data sources,
    generates explainability factors, and returns the complete assessment.
    """
    # Business rule validation
    validation = validate_application_data(application)
    if not validation["valid"]:
        raise HTTPException(status_code=400, detail="; ".join(validation["errors"]))

    # Check if customer already exists (by phone)
    existing = db.query(Customer).filter(
        Customer.phone_number == application.phone_number
    ).first()

    if existing:
        customer = existing
        customer.name = application.name
        customer.email = application.email
        customer.loan_amount_requested = application.loan_amount_requested
    else:
        customer = Customer(
            name=application.name,
            phone_number=application.phone_number,
            email=application.email,
            date_of_birth=application.date_of_birth,
            occupation=application.occupation,
            loan_amount_requested=application.loan_amount_requested,
        )
        db.add(customer)

    db.flush()

    # Calculate scores
    scores = calculate_credit_score(application)

    # Generate explanations
    input_dict = application.model_dump()
    # Convert nested pydantic models to dicts for explainability
    for key in ["gst_data", "upi_data", "telecom_data", "utility_data", "ecommerce_data", "mobility_data"]:
        if key in input_dict and input_dict[key] is not None:
            pass  # already a dict from model_dump

    explanation = generate_explanation(scores, input_dict)

    # Create credit score record
    credit_score = CreditScore(
        customer_id=customer.customer_id,
        overall_risk_score=scores["overall_risk_score"],
        risk_category=scores["risk_category"],
        gst_score=scores["gst_score"],
        upi_score=scores["upi_score"],
        telecom_score=scores["telecom_score"],
        utility_score=scores["utility_score"],
        ecommerce_score=scores["ecommerce_score"],
        mobility_score=scores["mobility_score"],
        confidence_level=scores["confidence_level"],
        explanation=explanation,
    )
    db.add(credit_score)
    db.commit()
    db.refresh(credit_score)

    return _build_score_output(credit_score)


@router.get("/credit/score/{score_id}", response_model=CreditScoreOutput)
async def get_credit_score(score_id: str, db: Session = Depends(get_db)):
    """Retrieve a previously calculated credit score by ID."""
    score = db.query(CreditScore).filter(CreditScore.score_id == score_id).first()
    if not score:
        raise HTTPException(status_code=404, detail="Score not found")
    return _build_score_output(score)


@router.get("/credit/customer/{customer_id}/scores", response_model=CustomerScoresResponse)
async def get_customer_scores(customer_id: str, db: Session = Depends(get_db)):
    """List all scores for a specific customer."""
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    scores = (
        db.query(CreditScore)
        .filter(CreditScore.customer_id == customer_id)
        .order_by(CreditScore.generated_at.desc())
        .all()
    )

    return CustomerScoresResponse(
        customer_id=customer.customer_id,
        customer_name=customer.name,
        scores=[
            CreditScoreListItem(
                score_id=s.score_id,
                overall_risk_score=s.overall_risk_score,
                risk_category=s.risk_category,
                confidence_level=s.confidence_level,
                generated_at=s.generated_at,
            )
            for s in scores
        ],
        total_count=len(scores),
    )


@router.post("/credit/compare", response_model=CompareResponse)
async def compare_customers(
    customer_id_1: str,
    customer_id_2: str,
    db: Session = Depends(get_db),
):
    """Compare the most recent risk profiles of two customers side-by-side."""
    score_1 = (
        db.query(CreditScore)
        .filter(CreditScore.customer_id == customer_id_1)
        .order_by(CreditScore.generated_at.desc())
        .first()
    )
    score_2 = (
        db.query(CreditScore)
        .filter(CreditScore.customer_id == customer_id_2)
        .order_by(CreditScore.generated_at.desc())
        .first()
    )

    result = CompareResponse()
    if score_1:
        result.customer_1 = _build_score_output(score_1)
    if score_2:
        result.customer_2 = _build_score_output(score_2)

    if not score_1 and not score_2:
        raise HTTPException(status_code=404, detail="No scores found for either customer")

    return result


@router.get("/credit/customers", response_model=List[CustomerListItem])
async def list_customers(db: Session = Depends(get_db)):
    """Fetch the latest 20 scored customers."""
    customers = db.query(Customer).order_by(Customer.created_at.desc()).limit(20).all()
    return [
        CustomerListItem(
            customer_id=c.customer_id,
            name=c.name,
            phone_number=c.phone_number,
            occupation=c.occupation,
            created_at=c.created_at
        ) for c in customers
    ]


@router.get("/credit/mock-customers")
async def list_mock_customers():
    """Return all mock customer profiles for demo purposes."""
    return get_all_mock_customers()


@router.get("/credit/mock-customers/{index}")
async def get_single_mock_customer(index: int):
    """Return a single mock customer by index (0-9)."""
    try:
        return get_mock_customer(index)
    except IndexError as e:
        raise HTTPException(status_code=404, detail=str(e))
