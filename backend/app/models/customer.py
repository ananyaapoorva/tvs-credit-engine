"""Customer database model."""

import enum
import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, Enum, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class OccupationType(str, enum.Enum):
    """Enumeration of supported occupation types."""
    GIG_WORKER = "gig_worker"
    SMALL_MERCHANT = "small_merchant"
    INFORMAL_SECTOR = "informal_sector"
    FIRST_TIME_BORROWER = "first_time_borrower"
    OTHER = "other"


class Customer(Base):
    """Customer model representing a credit application applicant."""

    __tablename__ = "customers"

    customer_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    occupation: Mapped[str] = mapped_column(
        Enum(OccupationType), nullable=False
    )
    loan_amount_requested: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    credit_scores = relationship("CreditScore", back_populates="customer")
    transactions = relationship("Transaction", back_populates="customer")

    def __repr__(self) -> str:
        return f"<Customer(id={self.customer_id}, name={self.name})>"
