"""Transaction database model for storing alternative data records."""

import enum
import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Enum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class TransactionType(str, enum.Enum):
    """Types of alternative data transactions."""
    GST = "gst"
    UPI = "upi"
    TELECOM = "telecom"
    UTILITY = "utility"
    ECOMMERCE = "ecommerce"
    MOBILITY = "mobility"


class Transaction(Base):
    """Transaction model for storing mock/real alternative data."""

    __tablename__ = "transactions"

    transaction_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    customer_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("customers.customer_id"), nullable=False
    )
    transaction_type: Mapped[str] = mapped_column(
        Enum(TransactionType), nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=True)

    # Relationships
    customer = relationship("Customer", back_populates="transactions")

    def __repr__(self) -> str:
        return (
            f"<Transaction(id={self.transaction_id}, "
            f"type={self.transaction_type}, "
            f"amount={self.amount})>"
        )
