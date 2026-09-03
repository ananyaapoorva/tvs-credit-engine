from typing import Optional, List, Dict
"""
Explainability service for generating human-readable risk factor explanations.

Provides transparent, detailed breakdowns of how each data source
contributes to the overall credit risk assessment.
"""


from app.utils.constants import (
    ECOMMERCE_WEIGHT,
    GST_WEIGHT,
    HIGH_RISK_THRESHOLD,
    MEDIUM_RISK_THRESHOLD,
    MOBILITY_WEIGHT,
    TELECOM_WEIGHT,
    UPI_WEIGHT,
    UTILITY_WEIGHT,
)


def _format_currency(amount: float) -> str:
    """Format a number as Indian currency string."""
    if amount >= 100000:
        return f"₹{amount / 100000:.1f}L"
    elif amount >= 1000:
        return f"₹{amount / 1000:.1f}K"
    else:
        return f"₹{amount:.0f}"


def generate_explanation(
    scores: Dict[str, float],
    input_data: dict,
) -> dict:
    """
    Generate human-readable explanations for credit score components.

    Args:
        scores: Dictionary of component scores (gst_score, upi_score, etc.)
        input_data: Original application input data for context.

    Returns:
        Dictionary with factors list, summary, and recommendation.
    """
    factors = []

    # ─── GST Explanations ────────────────────────────────────────────
    gst_score = scores.get("gst_score", 0)
    gst_data = input_data.get("gst_data", {})
    turnover = gst_data.get("annual_turnover", 0)
    filing = gst_data.get("filing_consistency", 0)

    if gst_score > 80:
        factors.append({
            "category": "GST Data",
            "signal": f"Strong GST filing history (turnover: {_format_currency(turnover)})",
            "impact": "positive",
            "contribution": f"+{GST_WEIGHT * 100:.0f}% weight applied",
            "explanation": "Consistent business records with solid turnover indicate strong financial discipline and reliable revenue stream."
        })
    elif gst_score > 40:
        factors.append({
            "category": "GST Data",
            "signal": f"Moderate GST activity (consistency: {filing * 100:.0f}%)",
            "impact": "neutral",
            "contribution": f"~{GST_WEIGHT * 100:.0f}% weight applied",
            "explanation": "GST records show moderate business activity. Improving filing consistency could strengthen your profile."
        })
    elif turnover > 0 or filing > 0:
        factors.append({
            "category": "GST Data",
            "signal": "Weak or irregular GST filings",
            "impact": "negative",
            "contribution": f"-{GST_WEIGHT * 100:.0f}% weight impact",
            "explanation": "Inconsistent GST records suggest irregular business activity or financial instability."
        })
    else:
        factors.append({
            "category": "GST Data",
            "signal": "No GST data provided",
            "impact": "neutral",
            "contribution": "0 points (no data)",
            "explanation": "GST data was not submitted. Providing this data could improve your score."
        })

    # ─── UPI Explanations ────────────────────────────────────────────
    upi_score = scores.get("upi_score", 0)
    upi_data = input_data.get("upi_data", {})
    upi_volume = upi_data.get("monthly_transaction_volume", 0)
    upi_freq = upi_data.get("transaction_frequency", 0)

    if upi_score > 80:
        factors.append({
            "category": "UPI Transactions",
            "signal": f"Strong monthly transaction volume ({_format_currency(upi_volume)}/month)",
            "impact": "positive",
            "contribution": f"+{UPI_WEIGHT * 100:.0f}% weight applied",
            "explanation": "Regular UPI activity demonstrates active digital financial participation and consistent income generation."
        })
    elif upi_score > 40:
        factors.append({
            "category": "UPI Transactions",
            "signal": f"Moderate UPI activity ({upi_freq} transactions/month)",
            "impact": "neutral",
            "contribution": f"~{UPI_WEIGHT * 100:.0f}% weight applied",
            "explanation": "UPI usage shows some digital financial activity but increasing volume could strengthen the profile."
        })
    elif upi_volume > 0 or upi_freq > 0:
        factors.append({
            "category": "UPI Transactions",
            "signal": "Low UPI transaction activity",
            "impact": "negative",
            "contribution": f"-{UPI_WEIGHT * 100:.0f}% weight impact",
            "explanation": "Limited UPI activity suggests lower digital financial engagement or inconsistent income patterns."
        })
    else:
        factors.append({
            "category": "UPI Transactions",
            "signal": "No UPI data provided",
            "impact": "neutral",
            "contribution": "0 points (no data)",
            "explanation": "UPI transaction data was not submitted. This is a key signal for income verification."
        })

    # ─── Telecom Explanations ────────────────────────────────────────
    telecom_score = scores.get("telecom_score", 0)
    telecom_data = input_data.get("telecom_data", {})
    telecom_consistency = telecom_data.get("recharge_consistency", 0)
    telecom_months = telecom_data.get("months_of_history", 0)

    if telecom_score > 80:
        factors.append({
            "category": "Telecom Consistency",
            "signal": f"{telecom_consistency * 100:.0f}% payment timeliness over {telecom_months} months",
            "impact": "positive",
            "contribution": f"+{TELECOM_WEIGHT * 100:.0f}% weight applied",
            "explanation": "Reliable telecom bill payments show financial discipline and capacity to meet regular obligations."
        })
    elif telecom_score > 40:
        factors.append({
            "category": "Telecom Consistency",
            "signal": f"Moderate telecom consistency ({telecom_consistency * 100:.0f}%)",
            "impact": "neutral",
            "contribution": f"~{TELECOM_WEIGHT * 100:.0f}% weight applied",
            "explanation": "Telecom payment history shows moderate reliability with room for improvement."
        })
    elif telecom_consistency > 0 or telecom_months > 0:
        factors.append({
            "category": "Telecom Consistency",
            "signal": "Inconsistent telecom recharge pattern",
            "impact": "negative",
            "contribution": f"-{TELECOM_WEIGHT * 100:.0f}% weight impact",
            "explanation": "Irregular recharge patterns indicate potential cash flow issues or financial instability."
        })
    else:
        factors.append({
            "category": "Telecom Consistency",
            "signal": "No telecom data provided",
            "impact": "neutral",
            "contribution": "0 points (no data)",
            "explanation": "Telecom data was not submitted. Regular recharge history demonstrates payment discipline."
        })

    # ─── Utility Explanations ────────────────────────────────────────
    utility_score = scores.get("utility_score", 0)
    utility_data = input_data.get("utility_data", {})
    utility_timeliness = utility_data.get("payment_timeliness", 0)

    if utility_score > 80:
        factors.append({
            "category": "Utility Payments",
            "signal": f"Excellent payment timeliness ({utility_timeliness * 100:.0f}% on-time)",
            "impact": "positive",
            "contribution": f"+{UTILITY_WEIGHT * 100:.0f}% weight applied",
            "explanation": "Consistent utility bill payments indicate residential stability and reliable financial habits."
        })
    elif utility_score > 40:
        factors.append({
            "category": "Utility Payments",
            "signal": f"Moderate payment pattern ({utility_timeliness * 100:.0f}% on-time)",
            "impact": "neutral",
            "contribution": f"~{UTILITY_WEIGHT * 100:.0f}% weight applied",
            "explanation": "Utility payment history shows some consistency but occasional delays noted."
        })
    elif utility_timeliness > 0:
        factors.append({
            "category": "Utility Payments",
            "signal": f"Occasional late payments ({utility_timeliness * 100:.0f}% on-time)",
            "impact": "negative",
            "contribution": f"-{UTILITY_WEIGHT * 100:.0f}% weight impact",
            "explanation": "Payment delays suggest cash flow constraints or financial stress periods."
        })
    else:
        factors.append({
            "category": "Utility Payments",
            "signal": "No utility data provided",
            "impact": "neutral",
            "contribution": "0 points (no data)",
            "explanation": "Utility payment data was not submitted. On-time bills demonstrate residential stability."
        })

    # ─── E-commerce Explanations ─────────────────────────────────────
    ecommerce_score = scores.get("ecommerce_score", 0)
    ecommerce_data = input_data.get("ecommerce_data", {})
    return_rate = ecommerce_data.get("return_rate", 0)
    purchase_freq = ecommerce_data.get("purchase_frequency", 0)

    if ecommerce_score > 80:
        factors.append({
            "category": "E-commerce Activity",
            "signal": f"Active buyer profile ({purchase_freq} purchases/month, {return_rate * 100:.0f}% returns)",
            "impact": "positive",
            "contribution": f"+{ECOMMERCE_WEIGHT * 100:.0f}% weight applied",
            "explanation": "Regular purchasing with low return rate indicates spending discipline and stable consumption patterns."
        })
    elif ecommerce_score > 40:
        factors.append({
            "category": "E-commerce Activity",
            "signal": f"Moderate e-commerce activity ({purchase_freq} purchases/month)",
            "impact": "neutral",
            "contribution": f"~{ECOMMERCE_WEIGHT * 100:.0f}% weight applied",
            "explanation": "E-commerce usage shows moderate digital engagement with average purchasing behavior."
        })
    elif purchase_freq > 0:
        factors.append({
            "category": "E-commerce Activity",
            "signal": "Limited e-commerce activity or high return rate",
            "impact": "negative",
            "contribution": f"-{ECOMMERCE_WEIGHT * 100:.0f}% weight impact",
            "explanation": "Low purchase frequency or high returns suggest uncertain spending patterns."
        })
    else:
        factors.append({
            "category": "E-commerce Activity",
            "signal": "No e-commerce data provided",
            "impact": "neutral",
            "contribution": "0 points (no data)",
            "explanation": "E-commerce activity data was not submitted."
        })

    # ─── Mobility Explanations ───────────────────────────────────────
    mobility_score = scores.get("mobility_score", 0)
    mobility_data = input_data.get("mobility_data", {})
    has_vehicle = mobility_data.get("vehicle_ownership", False)
    vehicle_type = mobility_data.get("vehicle_type", "none")

    if mobility_score > 80:
        factors.append({
            "category": "Mobility & Vehicle",
            "signal": f"Vehicle owner ({vehicle_type}) with consistent usage",
            "impact": "positive",
            "contribution": f"+{MOBILITY_WEIGHT * 100:.0f}% weight applied",
            "explanation": "Vehicle ownership and consistent fuel spending indicate asset ownership and stable mobility patterns."
        })
    elif mobility_score > 40:
        factors.append({
            "category": "Mobility & Vehicle",
            "signal": f"Moderate mobility data ({'owns ' + vehicle_type if has_vehicle else 'no vehicle'})",
            "impact": "neutral",
            "contribution": f"~{MOBILITY_WEIGHT * 100:.0f}% weight applied",
            "explanation": "Some mobility data available but limited tracking history."
        })
    elif has_vehicle:
        factors.append({
            "category": "Mobility & Vehicle",
            "signal": "Vehicle owned but limited tracking data",
            "impact": "neutral",
            "contribution": f"~{MOBILITY_WEIGHT * 100:.0f}% weight applied",
            "explanation": "Vehicle ownership is positive but more tracking data would strengthen the assessment."
        })
    else:
        factors.append({
            "category": "Mobility & Vehicle",
            "signal": "No vehicle or mobility data",
            "impact": "neutral",
            "contribution": "0 points (no data)",
            "explanation": "No vehicle ownership or mobility data submitted."
        })

    # ─── Generate Summary ────────────────────────────────────────────
    overall = scores.get("overall_risk_score", 0)
    positive_factors = [f for f in factors if f["impact"] == "positive"]
    negative_factors = [f for f in factors if f["impact"] == "negative"]

    if len(positive_factors) > len(negative_factors):
        pos_cats = ", ".join([f["category"] for f in positive_factors[:2]])
        summary = (
            f"Your application shows strong signals in {pos_cats}. "
            f"These demonstrate reliable financial behavior and active economic participation."
        )
    elif len(negative_factors) > len(positive_factors):
        neg_cats = ", ".join([f["category"] for f in negative_factors[:2]])
        summary = (
            f"Your application has areas needing improvement in {neg_cats}. "
            f"Strengthening these areas would significantly improve your credit profile."
        )
    else:
        summary = (
            "Your application shows a balanced profile with both strengths and areas for improvement. "
            "Providing additional data sources could improve your confidence score."
        )

    # ─── Generate Recommendation ─────────────────────────────────────
    if overall >= MEDIUM_RISK_THRESHOLD:
        recommendation = (
            "Loan approval recommended at standard interest rates. "
            "Strong alternative data signals support creditworthiness."
        )
    elif overall >= HIGH_RISK_THRESHOLD:
        recommendation = (
            "Loan approval recommended with enhanced monitoring. "
            "Consider automatic payment setup to improve timeliness scores."
        )
    else:
        recommendation = (
            "Loan requires additional review. Consider requesting more data sources "
            "or a smaller loan amount to improve approval chances."
        )

    return {
        "factors": factors,
        "summary": summary,
        "recommendation": recommendation,
    }
