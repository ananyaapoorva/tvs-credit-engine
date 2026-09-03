from typing import Optional, List, Dict
"""Pydantic schemas for credit application input validation."""

from datetime import date

from pydantic import BaseModel, Field, field_validator


class GSTData(BaseModel):
    """GST filing and turnover data."""
    annual_turnover: float = Field(default=0, ge=0, description="Annual GST turnover in INR")
    filing_consistency: float = Field(default=0, ge=0, le=1, description="Filing consistency ratio (0-1)")
    months_filed: int = Field(default=0, ge=0, le=12, description="Months filed in last 12")
    business_type: str = Field(default="other", description="Business category")


class UPIData(BaseModel):
    """UPI transaction trend data."""
    monthly_transaction_volume: float = Field(default=0, ge=0, description="Monthly UPI volume in INR")
    transaction_frequency: int = Field(default=0, ge=0, description="Transactions per month")
    average_transaction_size: float = Field(default=0, ge=0, description="Average transaction amount INR")
    months_active: int = Field(default=0, ge=0, description="Months with UPI activity")


class TelecomData(BaseModel):
    """Telecom recharge pattern data."""
    monthly_recharge_amount: float = Field(default=0, ge=0, description="Monthly recharge in INR")
    recharge_consistency: float = Field(default=0, ge=0, le=1, description="Recharge consistency ratio (0-1)")
    months_of_history: int = Field(default=0, ge=0, description="Months of telecom history")


class UtilityData(BaseModel):
    """Utility bill payment data."""
    monthly_bill_amount: float = Field(default=0, ge=0, description="Average monthly bill in INR")
    payment_timeliness: float = Field(default=0, ge=0, le=1, description="On-time payment ratio (0-1)")
    months_of_history: int = Field(default=0, ge=0, description="Months of utility history")


class EcommerceData(BaseModel):
    """E-commerce activity data."""
    purchase_frequency: int = Field(default=0, ge=0, description="Purchases per month")
    average_order_value: float = Field(default=0, ge=0, description="Average order value in INR")
    return_rate: float = Field(default=0, ge=0, le=1, description="Product return rate (0-1)")
    months_active: int = Field(default=0, ge=0, description="Months with e-commerce activity")


class MobilityData(BaseModel):
    """Mobility and vehicle usage data."""
    vehicle_ownership: bool = Field(default=False, description="Whether applicant owns a vehicle")
    vehicle_type: str = Field(default="none", description="Type of vehicle")
    fuel_expense_monthly: float = Field(default=0, ge=0, description="Monthly fuel expense in INR")
    months_tracked: int = Field(default=0, ge=0, description="Months of mobility data")


class CreditApplicationInput(BaseModel):
    """Complete credit application input schema."""
    name: str = Field(..., min_length=2, max_length=255, description="Full name of the applicant")
    phone_number: str = Field(..., description="Indian mobile number (10 digits)")
    email: str = Field(..., description="Email address")
    date_of_birth: date = Field(..., description="Date of birth")
    occupation: str = Field(..., description="Occupation type")
    loan_amount_requested: float = Field(..., gt=0, description="Requested loan amount in INR")
    gst_data: Optional[GSTData] = Field(default_factory=GSTData)
    upi_data: Optional[UPIData] = Field(default_factory=UPIData)
    telecom_data: Optional[TelecomData] = Field(default_factory=TelecomData)
    utility_data: Optional[UtilityData] = Field(default_factory=UtilityData)
    ecommerce_data: Optional[EcommerceData] = Field(default_factory=EcommerceData)
    mobility_data: Optional[MobilityData] = Field(default_factory=MobilityData)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Basic email validation."""
        if "@" not in v or "." not in v:
            raise ValueError("Invalid email address")
        return v

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """Validate Indian phone number format."""
        cleaned = v.strip().replace(" ", "").replace("-", "")
        if len(cleaned) == 13 and cleaned.startswith("+91"):
            cleaned = cleaned[3:]
        elif len(cleaned) == 12 and cleaned.startswith("91"):
            cleaned = cleaned[2:]
        if len(cleaned) != 10 or not cleaned.isdigit():
            raise ValueError("Phone number must be 10 digits")
        if cleaned[0] not in "6789":
            raise ValueError("Indian phone number must start with 6, 7, 8, or 9")
        return cleaned

    @field_validator("occupation")
    @classmethod
    def validate_occupation(cls, v: str) -> str:
        """Validate occupation type."""
        valid = {"gig_worker", "small_merchant", "informal_sector", "first_time_borrower", "other"}
        if v not in valid:
            raise ValueError(f"Occupation must be one of: {', '.join(valid)}")
        return v
