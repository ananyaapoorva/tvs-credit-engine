"""
Core credit scoring engine implementing deterministic, rule-based scoring.

Processes 6 alternative data sources (GST, UPI, Telecom, Utility,
E-commerce, Mobility) to generate an overall risk score with
transparent, explainable component breakdowns.
"""

from app.schemas.credit_input import (
    CreditApplicationInput, GSTData, UPIData,
    TelecomData, UtilityData, EcommerceData, MobilityData,
)
from app.utils.constants import (
    GST_WEIGHT, UPI_WEIGHT, TELECOM_WEIGHT, UTILITY_WEIGHT,
    ECOMMERCE_WEIGHT, MOBILITY_WEIGHT,
    HIGH_RISK_THRESHOLD, MEDIUM_RISK_THRESHOLD,
    MIN_SCORE, MAX_SCORE,
    GST_HIGH_TURNOVER, GST_HIGH_CONSISTENCY, GST_HIGH_MONTHS,
    GST_HIGH_RISK_BUSINESS_TYPES, GST_TURNOVER_POINTS,
    GST_CONSISTENCY_POINTS, GST_FREQUENCY_POINTS, GST_MAX_POINTS,
    GST_RISK_DEDUCTION,
    UPI_HIGH_VOLUME, UPI_HIGH_FREQUENCY, UPI_HIGH_MONTHS,
    UPI_AVG_SIZE_THRESHOLD, UPI_VOLUME_POINTS, UPI_FREQUENCY_POINTS,
    UPI_DURATION_POINTS, UPI_AVG_SIZE_POINTS, UPI_MAX_POINTS,
    TELECOM_HIGH_CONSISTENCY, TELECOM_MIN_RECHARGE, TELECOM_HIGH_MONTHS,
    TELECOM_CONSISTENCY_POINTS, TELECOM_AMOUNT_POINTS,
    TELECOM_HISTORY_POINTS, TELECOM_GAPS_POINTS, TELECOM_MAX_POINTS,
    UTILITY_HIGH_TIMELINESS, UTILITY_MIN_BILL, UTILITY_HIGH_MONTHS,
    UTILITY_TIMELINESS_POINTS, UTILITY_BILL_AMOUNT_POINTS,
    UTILITY_HISTORY_POINTS, UTILITY_PATTERN_POINTS, UTILITY_MAX_POINTS,
    ECOMMERCE_HIGH_FREQUENCY, ECOMMERCE_LOW_RETURN_RATE,
    ECOMMERCE_HIGH_AOV, ECOMMERCE_HIGH_MONTHS,
    ECOMMERCE_FREQUENCY_POINTS, ECOMMERCE_RETURN_POINTS,
    ECOMMERCE_AOV_POINTS, ECOMMERCE_DURATION_POINTS, ECOMMERCE_MAX_POINTS,
    MOBILITY_OWNERSHIP_POINTS, MOBILITY_CONSISTENCY_POINTS,
    MOBILITY_DURATION_POINTS, MOBILITY_HIGH_MONTHS,
    MOBILITY_MIN_FUEL_EXPENSE, MOBILITY_MAX_POINTS,
    VEHICLE_TYPE_SCORES, TOTAL_DATA_FIELDS,
)


def _clamp(value: float) -> float:
    """Clamp a score between MIN_SCORE and MAX_SCORE."""
    return max(MIN_SCORE, min(MAX_SCORE, value))


def _normalize(raw: float, max_points: float) -> float:
    """Normalize raw points to a 0-100 scale."""
    if max_points <= 0:
        return 0.0
    return _clamp((raw / max_points) * MAX_SCORE)


def score_gst_data(data: GSTData) -> float:
    """
    Score GST data based on turnover, filing consistency, and months filed.

    Returns a score from 0-100.
    """
    raw = 0.0

    # Turnover score (proportional up to threshold)
    if data.annual_turnover >= GST_HIGH_TURNOVER:
        raw += GST_TURNOVER_POINTS
    elif data.annual_turnover > 0:
        raw += GST_TURNOVER_POINTS * (data.annual_turnover / GST_HIGH_TURNOVER)

    # Filing consistency score
    if data.filing_consistency >= GST_HIGH_CONSISTENCY:
        raw += GST_CONSISTENCY_POINTS
    elif data.filing_consistency > 0:
        raw += GST_CONSISTENCY_POINTS * (data.filing_consistency / GST_HIGH_CONSISTENCY)

    # Months filed score
    if data.months_filed >= GST_HIGH_MONTHS:
        raw += GST_FREQUENCY_POINTS
    elif data.months_filed > 0:
        raw += GST_FREQUENCY_POINTS * (data.months_filed / GST_HIGH_MONTHS)

    # High-risk business type deduction
    if data.business_type.lower() in GST_HIGH_RISK_BUSINESS_TYPES:
        raw -= GST_RISK_DEDUCTION

    return _normalize(max(raw, 0), GST_MAX_POINTS)


def score_upi_data(data: UPIData) -> float:
    """
    Score UPI data based on transaction volume, frequency, duration, and size.

    Returns a score from 0-100.
    """
    raw = 0.0

    # Volume score
    if data.monthly_transaction_volume >= UPI_HIGH_VOLUME:
        raw += UPI_VOLUME_POINTS
    elif data.monthly_transaction_volume > 0:
        raw += UPI_VOLUME_POINTS * (data.monthly_transaction_volume / UPI_HIGH_VOLUME)

    # Frequency score
    if data.transaction_frequency >= UPI_HIGH_FREQUENCY:
        raw += UPI_FREQUENCY_POINTS
    elif data.transaction_frequency > 0:
        raw += UPI_FREQUENCY_POINTS * (data.transaction_frequency / UPI_HIGH_FREQUENCY)

    # Duration score
    if data.months_active >= UPI_HIGH_MONTHS:
        raw += UPI_DURATION_POINTS
    elif data.months_active > 0:
        raw += UPI_DURATION_POINTS * (data.months_active / UPI_HIGH_MONTHS)

    # Average transaction size stability score
    if data.average_transaction_size >= UPI_AVG_SIZE_THRESHOLD:
        raw += UPI_AVG_SIZE_POINTS
    elif data.average_transaction_size > 0:
        raw += UPI_AVG_SIZE_POINTS * (data.average_transaction_size / UPI_AVG_SIZE_THRESHOLD)

    return _normalize(raw, UPI_MAX_POINTS)


def score_telecom_data(data: TelecomData) -> float:
    """
    Score telecom data based on recharge consistency, amount, and history.

    Returns a score from 0-100.
    """
    raw = 0.0

    # Consistency score
    if data.recharge_consistency >= TELECOM_HIGH_CONSISTENCY:
        raw += TELECOM_CONSISTENCY_POINTS
    elif data.recharge_consistency > 0:
        raw += TELECOM_CONSISTENCY_POINTS * (data.recharge_consistency / TELECOM_HIGH_CONSISTENCY)

    # Recharge amount score
    if data.monthly_recharge_amount >= TELECOM_MIN_RECHARGE:
        raw += TELECOM_AMOUNT_POINTS
    elif data.monthly_recharge_amount > 0:
        raw += TELECOM_AMOUNT_POINTS * (data.monthly_recharge_amount / TELECOM_MIN_RECHARGE)

    # History duration score
    if data.months_of_history >= TELECOM_HIGH_MONTHS:
        raw += TELECOM_HISTORY_POINTS
    elif data.months_of_history > 0:
        raw += TELECOM_HISTORY_POINTS * (data.months_of_history / TELECOM_HIGH_MONTHS)

    # Gaps score (derived from consistency — high consistency = no gaps)
    if data.recharge_consistency >= TELECOM_HIGH_CONSISTENCY:
        raw += TELECOM_GAPS_POINTS
    elif data.recharge_consistency >= 0.7:
        raw += TELECOM_GAPS_POINTS * 0.6

    return _normalize(raw, TELECOM_MAX_POINTS)


def score_utility_data(data: UtilityData) -> float:
    """
    Score utility data based on bill payment timeliness, amount, and history.

    Returns a score from 0-100.
    """
    raw = 0.0

    # Payment timeliness score
    if data.payment_timeliness >= UTILITY_HIGH_TIMELINESS:
        raw += UTILITY_TIMELINESS_POINTS
    elif data.payment_timeliness > 0:
        raw += UTILITY_TIMELINESS_POINTS * (data.payment_timeliness / UTILITY_HIGH_TIMELINESS)

    # Bill amount score (indicates residential stability)
    if data.monthly_bill_amount >= UTILITY_MIN_BILL:
        raw += UTILITY_BILL_AMOUNT_POINTS
    elif data.monthly_bill_amount > 0:
        raw += UTILITY_BILL_AMOUNT_POINTS * (data.monthly_bill_amount / UTILITY_MIN_BILL)

    # History duration score
    if data.months_of_history >= UTILITY_HIGH_MONTHS:
        raw += UTILITY_HISTORY_POINTS
    elif data.months_of_history > 0:
        raw += UTILITY_HISTORY_POINTS * (data.months_of_history / UTILITY_HIGH_MONTHS)

    # Regular payment pattern (derived from timeliness + history)
    if data.payment_timeliness >= UTILITY_HIGH_TIMELINESS and data.months_of_history >= UTILITY_HIGH_MONTHS:
        raw += UTILITY_PATTERN_POINTS
    elif data.payment_timeliness >= 0.6 and data.months_of_history >= 6:
        raw += UTILITY_PATTERN_POINTS * 0.5

    return _normalize(raw, UTILITY_MAX_POINTS)


def score_ecommerce_data(data: EcommerceData) -> float:
    """
    Score e-commerce data based on purchase frequency, return rate, and order value.

    Returns a score from 0-100.
    """
    raw = 0.0

    # Purchase frequency score
    if data.purchase_frequency >= ECOMMERCE_HIGH_FREQUENCY:
        raw += ECOMMERCE_FREQUENCY_POINTS
    elif data.purchase_frequency > 0:
        raw += ECOMMERCE_FREQUENCY_POINTS * (data.purchase_frequency / ECOMMERCE_HIGH_FREQUENCY)

    # Return rate score (lower is better)
    if data.return_rate <= ECOMMERCE_LOW_RETURN_RATE:
        raw += ECOMMERCE_RETURN_POINTS
    elif data.return_rate < 0.3:
        raw += ECOMMERCE_RETURN_POINTS * ((0.3 - data.return_rate) / 0.2)

    # Average order value score
    if data.average_order_value >= ECOMMERCE_HIGH_AOV:
        raw += ECOMMERCE_AOV_POINTS
    elif data.average_order_value > 0:
        raw += ECOMMERCE_AOV_POINTS * (data.average_order_value / ECOMMERCE_HIGH_AOV)

    # Duration score
    if data.months_active >= ECOMMERCE_HIGH_MONTHS:
        raw += ECOMMERCE_DURATION_POINTS
    elif data.months_active > 0:
        raw += ECOMMERCE_DURATION_POINTS * (data.months_active / ECOMMERCE_HIGH_MONTHS)

    return _normalize(raw, ECOMMERCE_MAX_POINTS)


def score_mobility_data(data: MobilityData) -> float:
    """
    Score mobility data based on vehicle ownership, fuel consistency, and duration.

    Returns a score from 0-100.
    """
    raw = 0.0

    # Vehicle ownership score
    if data.vehicle_ownership:
        raw += MOBILITY_OWNERSHIP_POINTS

    # Fuel expense consistency (indicates regular usage)
    if data.fuel_expense_monthly >= MOBILITY_MIN_FUEL_EXPENSE:
        raw += MOBILITY_CONSISTENCY_POINTS
    elif data.fuel_expense_monthly > 0:
        raw += MOBILITY_CONSISTENCY_POINTS * (data.fuel_expense_monthly / MOBILITY_MIN_FUEL_EXPENSE)

    # Tracking duration score
    if data.months_tracked >= MOBILITY_HIGH_MONTHS:
        raw += MOBILITY_DURATION_POINTS
    elif data.months_tracked > 0:
        raw += MOBILITY_DURATION_POINTS * (data.months_tracked / MOBILITY_HIGH_MONTHS)

    # Vehicle type score
    vehicle_type_score = VEHICLE_TYPE_SCORES.get(data.vehicle_type.lower(), 0)
    raw += vehicle_type_score

    return _normalize(raw, MOBILITY_MAX_POINTS)


def categorize_risk(score: float) -> str:
    """
    Categorize risk based on overall score.

    0-40: HIGH RISK
    40-70: MEDIUM RISK
    70-100: LOW RISK
    """
    if score < HIGH_RISK_THRESHOLD:
        return "high"
    elif score < MEDIUM_RISK_THRESHOLD:
        return "medium"
    else:
        return "low"


def calculate_confidence(data: CreditApplicationInput) -> float:
    """
    Calculate confidence level based on data completeness.

    Returns a percentage (0-100) indicating how many data sources
    have meaningful data provided.
    """
    sources_provided = 0

    # Check each data source for meaningful data
    if data.gst_data and (data.gst_data.annual_turnover > 0 or data.gst_data.months_filed > 0):
        sources_provided += 1

    if data.upi_data and (data.upi_data.monthly_transaction_volume > 0 or data.upi_data.months_active > 0):
        sources_provided += 1

    if data.telecom_data and (data.telecom_data.monthly_recharge_amount > 0 or data.telecom_data.months_of_history > 0):
        sources_provided += 1

    if data.utility_data and (data.utility_data.monthly_bill_amount > 0 or data.utility_data.months_of_history > 0):
        sources_provided += 1

    if data.ecommerce_data and (data.ecommerce_data.purchase_frequency > 0 or data.ecommerce_data.months_active > 0):
        sources_provided += 1

    if data.mobility_data and (data.mobility_data.vehicle_ownership or data.mobility_data.fuel_expense_monthly > 0):
        sources_provided += 1

    return _clamp((sources_provided / TOTAL_DATA_FIELDS) * MAX_SCORE)


def calculate_credit_score(application_data: CreditApplicationInput) -> dict:
    """
    Calculate the complete credit score from application data.

    Processes all 6 alternative data sources, applies weights,
    and returns the overall score with component breakdowns.

    Args:
        application_data: Validated credit application input.

    Returns:
        Dictionary containing overall score, component scores,
        risk category, and confidence level.
    """
    # Calculate individual component scores
    gst = score_gst_data(application_data.gst_data)
    upi = score_upi_data(application_data.upi_data)
    telecom = score_telecom_data(application_data.telecom_data)
    utility = score_utility_data(application_data.utility_data)
    ecommerce = score_ecommerce_data(application_data.ecommerce_data)
    mobility = score_mobility_data(application_data.mobility_data)

    # Calculate weighted overall score
    overall = (
        gst * GST_WEIGHT
        + upi * UPI_WEIGHT
        + telecom * TELECOM_WEIGHT
        + utility * UTILITY_WEIGHT
        + ecommerce * ECOMMERCE_WEIGHT
        + mobility * MOBILITY_WEIGHT
    )
    overall = _clamp(round(overall, 2))

    # Determine risk category and confidence
    risk_category = categorize_risk(overall)
    confidence = calculate_confidence(application_data)

    return {
        "overall_risk_score": overall,
        "risk_category": risk_category,
        "gst_score": round(gst, 2),
        "upi_score": round(upi, 2),
        "telecom_score": round(telecom, 2),
        "utility_score": round(utility, 2),
        "ecommerce_score": round(ecommerce, 2),
        "mobility_score": round(mobility, 2),
        "confidence_level": round(confidence, 2),
    }
