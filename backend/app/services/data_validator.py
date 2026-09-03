"""Data validation service for credit application inputs."""

from app.schemas.credit_input import CreditApplicationInput


def validate_application_data(data: CreditApplicationInput) -> dict:
    """
    Perform additional business rule validation on application data.

    Returns a dict with 'valid' boolean and 'errors' list.
    Pydantic handles type/range validation; this adds business logic checks.
    """
    errors = []

    # Age validation (must be 18+ years old)
    from datetime import date
    today = date.today()
    age = (
        today.year - data.date_of_birth.year
        - ((today.month, today.day) < (data.date_of_birth.month, data.date_of_birth.day))
    )
    if age < 18:
        errors.append("Applicant must be at least 18 years old")
    if age > 100:
        errors.append("Invalid date of birth")

    # Loan amount sanity check
    if data.loan_amount_requested > 10000000:  # ₹1 crore max
        errors.append("Loan amount exceeds maximum allowed (₹1,00,00,000)")
    if data.loan_amount_requested < 1000:  # ₹1K minimum
        errors.append("Loan amount below minimum threshold (₹1,000)")

    # GST data cross-validation
    if data.gst_data:
        if data.gst_data.months_filed > 12:
            errors.append("GST months filed cannot exceed 12")
        if data.gst_data.filing_consistency > 1:
            errors.append("GST filing consistency cannot exceed 100%")

    # UPI data sanity
    if data.upi_data:
        if data.upi_data.months_active > 120:  # 10 years
            errors.append("UPI months active seems unrealistic (>10 years)")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }
