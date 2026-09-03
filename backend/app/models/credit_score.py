"""Credit score database model."""

import enum
import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, Enum, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class RiskCategory(str, enum.Enum):
    """Risk classification categories."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class CreditScore(Base):
    """Credit score model storing calculated risk assessment results."""

    __tablename__ = "credit_scores"

    score_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    customer_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("customers.customer_id"), nullable=False
    )
    overall_risk_score: Mapped[float] = mapped_column(Float, nullable=False)
    risk_category: Mapped[str] = mapped_column(
        Enum(RiskCategory), nullable=False
    )
    gst_score: Mapped[float] = mapped_column(Float, default=0.0)
    upi_score: Mapped[float] = mapped_column(Float, default=0.0)
    telecom_score: Mapped[float] = mapped_column(Float, default=0.0)
    utility_score: Mapped[float] = mapped_column(Float, default=0.0)
    ecommerce_score: Mapped[float] = mapped_column(Float, default=0.0)
    mobility_score: Mapped[float] = mapped_column(Float, default=0.0)
    confidence_level: Mapped[float] = mapped_column(Float, default=0.0)
    explanation: Mapped[dict] = mapped_column(JSON, nullable=True)
    generated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relationships
    customer = relationship("Customer", back_populates="credit_scores")

    def __repr__(self) -> str:
        return (
            f"<CreditScore(id={self.score_id}, "
            f"score={self.overall_risk_score}, "
            f"risk={self.risk_category})>"
        )
