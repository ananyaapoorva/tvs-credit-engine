"""
Tests for the explainability service.

Verifies correct generation of human-readable explanations
for credit score components.
"""

import pytest
from app.services.explainability import generate_explanation, _format_currency


class TestFormatCurrency:
    def test_lakhs(self):
        assert _format_currency(500000) == "₹5.0L"

    def test_thousands(self):
        assert _format_currency(5000) == "₹5.0K"

    def test_small_amount(self):
        assert _format_currency(500) == "₹500"


class TestGenerateExplanation:
    def test_positive_gst_factor(self):
        scores = {"gst_score": 85, "upi_score": 0, "telecom_score": 0,
                  "utility_score": 0, "ecommerce_score": 0, "mobility_score": 0,
                  "overall_risk_score": 17}
        input_data = {
            "gst_data": {"annual_turnover": 500000, "filing_consistency": 0.95},
            "upi_data": {}, "telecom_data": {}, "utility_data": {},
            "ecommerce_data": {}, "mobility_data": {},
        }
        result = generate_explanation(scores, input_data)
        gst_factor = result["factors"][0]
        assert gst_factor["category"] == "GST Data"
        assert gst_factor["impact"] == "positive"

    def test_negative_gst_factor(self):
        scores = {"gst_score": 30, "upi_score": 0, "telecom_score": 0,
                  "utility_score": 0, "ecommerce_score": 0, "mobility_score": 0,
                  "overall_risk_score": 6}
        input_data = {
            "gst_data": {"annual_turnover": 50000, "filing_consistency": 0.3},
            "upi_data": {}, "telecom_data": {}, "utility_data": {},
            "ecommerce_data": {}, "mobility_data": {},
        }
        result = generate_explanation(scores, input_data)
        gst_factor = result["factors"][0]
        assert gst_factor["category"] == "GST Data"
        assert gst_factor["impact"] == "negative"

    def test_no_gst_data(self):
        scores = {"gst_score": 0, "upi_score": 0, "telecom_score": 0,
                  "utility_score": 0, "ecommerce_score": 0, "mobility_score": 0,
                  "overall_risk_score": 0}
        input_data = {
            "gst_data": {"annual_turnover": 0, "filing_consistency": 0},
            "upi_data": {}, "telecom_data": {}, "utility_data": {},
            "ecommerce_data": {}, "mobility_data": {},
        }
        result = generate_explanation(scores, input_data)
        gst_factor = result["factors"][0]
        assert gst_factor["impact"] == "neutral"

    def test_positive_upi_factor(self):
        scores = {"gst_score": 0, "upi_score": 90, "telecom_score": 0,
                  "utility_score": 0, "ecommerce_score": 0, "mobility_score": 0,
                  "overall_risk_score": 18}
        input_data = {
            "gst_data": {}, "upi_data": {"monthly_transaction_volume": 150000, "transaction_frequency": 30},
            "telecom_data": {}, "utility_data": {},
            "ecommerce_data": {}, "mobility_data": {},
        }
        result = generate_explanation(scores, input_data)
        upi_factor = [f for f in result["factors"] if f["category"] == "UPI Transactions"][0]
        assert upi_factor["impact"] == "positive"

    def test_all_factors_present(self):
        scores = {"gst_score": 85, "upi_score": 78, "telecom_score": 92,
                  "utility_score": 70, "ecommerce_score": 68, "mobility_score": 75,
                  "overall_risk_score": 78}
        input_data = {
            "gst_data": {"annual_turnover": 500000, "filing_consistency": 0.95},
            "upi_data": {"monthly_transaction_volume": 120000, "transaction_frequency": 25},
            "telecom_data": {"recharge_consistency": 0.95, "months_of_history": 24},
            "utility_data": {"payment_timeliness": 0.82},
            "ecommerce_data": {"purchase_frequency": 5, "return_rate": 0.05},
            "mobility_data": {"vehicle_ownership": True, "vehicle_type": "two_wheeler"},
        }
        result = generate_explanation(scores, input_data)
        assert len(result["factors"]) == 6  # One factor per category
        categories = {f["category"] for f in result["factors"]}
        assert "GST Data" in categories
        assert "UPI Transactions" in categories
        assert "Telecom Consistency" in categories
        assert "Utility Payments" in categories
        assert "E-commerce Activity" in categories
        assert "Mobility & Vehicle" in categories

    def test_summary_generated(self):
        scores = {"gst_score": 85, "upi_score": 78, "telecom_score": 92,
                  "utility_score": 70, "ecommerce_score": 68, "mobility_score": 75,
                  "overall_risk_score": 78}
        input_data = {
            "gst_data": {"annual_turnover": 500000, "filing_consistency": 0.95},
            "upi_data": {"monthly_transaction_volume": 120000, "transaction_frequency": 25},
            "telecom_data": {"recharge_consistency": 0.95, "months_of_history": 24},
            "utility_data": {"payment_timeliness": 0.82},
            "ecommerce_data": {"purchase_frequency": 5, "return_rate": 0.05},
            "mobility_data": {"vehicle_ownership": True, "vehicle_type": "two_wheeler"},
        }
        result = generate_explanation(scores, input_data)
        assert len(result["summary"]) > 10
        assert len(result["recommendation"]) > 10

    def test_low_risk_recommendation(self):
        scores = {"gst_score": 90, "upi_score": 85, "telecom_score": 95,
                  "utility_score": 80, "ecommerce_score": 75, "mobility_score": 80,
                  "overall_risk_score": 85}
        input_data = {
            "gst_data": {"annual_turnover": 500000, "filing_consistency": 0.95},
            "upi_data": {"monthly_transaction_volume": 120000, "transaction_frequency": 25},
            "telecom_data": {"recharge_consistency": 0.95, "months_of_history": 24},
            "utility_data": {"payment_timeliness": 0.9},
            "ecommerce_data": {"purchase_frequency": 5, "return_rate": 0.05},
            "mobility_data": {"vehicle_ownership": True, "vehicle_type": "car"},
        }
        result = generate_explanation(scores, input_data)
        assert "approval" in result["recommendation"].lower() or "recommend" in result["recommendation"].lower()

    def test_high_risk_recommendation(self):
        scores = {"gst_score": 10, "upi_score": 15, "telecom_score": 20,
                  "utility_score": 10, "ecommerce_score": 5, "mobility_score": 0,
                  "overall_risk_score": 10}
        input_data = {
            "gst_data": {"annual_turnover": 30000, "filing_consistency": 0.2},
            "upi_data": {"monthly_transaction_volume": 5000, "transaction_frequency": 2},
            "telecom_data": {"recharge_consistency": 0.3, "months_of_history": 3},
            "utility_data": {"payment_timeliness": 0.3},
            "ecommerce_data": {"purchase_frequency": 0},
            "mobility_data": {"vehicle_ownership": False},
        }
        result = generate_explanation(scores, input_data)
        assert "review" in result["recommendation"].lower() or "additional" in result["recommendation"].lower()

    def test_factor_structure(self):
        scores = {"gst_score": 50, "upi_score": 50, "telecom_score": 50,
                  "utility_score": 50, "ecommerce_score": 50, "mobility_score": 50,
                  "overall_risk_score": 50}
        input_data = {
            "gst_data": {"annual_turnover": 200000, "filing_consistency": 0.6},
            "upi_data": {"monthly_transaction_volume": 50000, "transaction_frequency": 12},
            "telecom_data": {"recharge_consistency": 0.7, "months_of_history": 10},
            "utility_data": {"payment_timeliness": 0.6},
            "ecommerce_data": {"purchase_frequency": 3, "return_rate": 0.12},
            "mobility_data": {"vehicle_ownership": True, "vehicle_type": "two_wheeler"},
        }
        result = generate_explanation(scores, input_data)
        for factor in result["factors"]:
            assert "category" in factor
            assert "signal" in factor
            assert "impact" in factor
            assert "contribution" in factor
            assert "explanation" in factor
            assert factor["impact"] in ["positive", "negative", "neutral"]
