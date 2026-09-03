"""
Comprehensive tests for the credit scoring engine.

Tests all 6 data source scorers, weighted combinations,
risk categorization, and edge cases.
"""

import pytest
from app.schemas.credit_input import (
    GSTData, UPIData, TelecomData, UtilityData,
    EcommerceData, MobilityData, CreditApplicationInput,
)
from app.services.scoring_engine import (
    score_gst_data, score_upi_data, score_telecom_data,
    score_utility_data, score_ecommerce_data, score_mobility_data,
    categorize_risk, calculate_confidence, calculate_credit_score,
    _clamp, _normalize,
)


# ─── Helper Fixtures ─────────────────────────────────────────────────────────

def _make_application(**overrides) -> CreditApplicationInput:
    """Create a test application with defaults."""
    defaults = {
        "name": "Test User",
        "phone_number": "9876543210",
        "email": "test@example.com",
        "date_of_birth": "1990-01-01",
        "occupation": "small_merchant",
        "loan_amount_requested": 50000,
    }
    defaults.update(overrides)
    return CreditApplicationInput(**defaults)


# ─── Clamp & Normalize Tests ────────────────────────────────────────────────

class TestClampNormalize:
    def test_clamp_within_bounds(self):
        assert _clamp(50.0) == 50.0

    def test_clamp_below_zero(self):
        assert _clamp(-10.0) == 0.0

    def test_clamp_above_hundred(self):
        assert _clamp(150.0) == 100.0

    def test_normalize_full_points(self):
        assert _normalize(60, 60) == 100.0

    def test_normalize_zero_points(self):
        assert _normalize(0, 60) == 0.0

    def test_normalize_half_points(self):
        assert _normalize(30, 60) == 50.0

    def test_normalize_zero_max(self):
        assert _normalize(10, 0) == 0.0


# ─── GST Score Tests ────────────────────────────────────────────────────────

class TestGSTScore:
    def test_high_turnover_high_consistency(self):
        data = GSTData(annual_turnover=500000, filing_consistency=0.95, months_filed=12, business_type="retail")
        score = score_gst_data(data)
        assert score > 80

    def test_low_turnover_low_consistency(self):
        data = GSTData(annual_turnover=50000, filing_consistency=0.3, months_filed=3, business_type="retail")
        score = score_gst_data(data)
        assert score < 40

    def test_zero_gst_data(self):
        data = GSTData(annual_turnover=0, filing_consistency=0, months_filed=0, business_type="other")
        score = score_gst_data(data)
        assert score == 0

    def test_high_risk_business_deduction(self):
        normal = GSTData(annual_turnover=400000, filing_consistency=0.9, months_filed=11, business_type="retail")
        risky = GSTData(annual_turnover=400000, filing_consistency=0.9, months_filed=11, business_type="gambling")
        assert score_gst_data(normal) > score_gst_data(risky)

    def test_max_gst_score(self):
        data = GSTData(annual_turnover=1000000, filing_consistency=1.0, months_filed=12, business_type="retail")
        score = score_gst_data(data)
        assert score == 100.0

    def test_proportional_scoring(self):
        low = GSTData(annual_turnover=150000, filing_consistency=0.5, months_filed=6, business_type="retail")
        high = GSTData(annual_turnover=300000, filing_consistency=0.9, months_filed=11, business_type="retail")
        assert score_gst_data(low) < score_gst_data(high)


# ─── UPI Score Tests ────────────────────────────────────────────────────────

class TestUPIScore:
    def test_high_volume_high_frequency(self):
        data = UPIData(monthly_transaction_volume=150000, transaction_frequency=30,
                       average_transaction_size=5000, months_active=24)
        score = score_upi_data(data)
        assert score > 80

    def test_low_volume_low_frequency(self):
        data = UPIData(monthly_transaction_volume=10000, transaction_frequency=3,
                       average_transaction_size=500, months_active=2)
        score = score_upi_data(data)
        assert score < 40

    def test_zero_upi_data(self):
        data = UPIData(monthly_transaction_volume=0, transaction_frequency=0,
                       average_transaction_size=0, months_active=0)
        score = score_upi_data(data)
        assert score == 0

    def test_months_active_threshold(self):
        short = UPIData(monthly_transaction_volume=80000, transaction_frequency=20,
                        average_transaction_size=2000, months_active=3)
        long = UPIData(monthly_transaction_volume=80000, transaction_frequency=20,
                       average_transaction_size=2000, months_active=24)
        assert score_upi_data(short) < score_upi_data(long)

    def test_max_upi_score(self):
        data = UPIData(monthly_transaction_volume=200000, transaction_frequency=50,
                       average_transaction_size=5000, months_active=24)
        score = score_upi_data(data)
        assert score == 100.0


# ─── Telecom Score Tests ────────────────────────────────────────────────────

class TestTelecomScore:
    def test_high_consistency(self):
        data = TelecomData(monthly_recharge_amount=400, recharge_consistency=0.95, months_of_history=24)
        score = score_telecom_data(data)
        assert score > 80

    def test_low_consistency(self):
        data = TelecomData(monthly_recharge_amount=100, recharge_consistency=0.3, months_of_history=3)
        score = score_telecom_data(data)
        assert score < 40

    def test_zero_telecom_data(self):
        data = TelecomData(monthly_recharge_amount=0, recharge_consistency=0, months_of_history=0)
        score = score_telecom_data(data)
        assert score == 0

    def test_max_telecom_score(self):
        data = TelecomData(monthly_recharge_amount=500, recharge_consistency=1.0, months_of_history=24)
        score = score_telecom_data(data)
        assert score == 100.0


# ─── Utility Score Tests ────────────────────────────────────────────────────

class TestUtilityScore:
    def test_high_timeliness(self):
        data = UtilityData(monthly_bill_amount=2000, payment_timeliness=0.95, months_of_history=18)
        score = score_utility_data(data)
        assert score > 80

    def test_low_timeliness(self):
        data = UtilityData(monthly_bill_amount=400, payment_timeliness=0.3, months_of_history=3)
        score = score_utility_data(data)
        assert score < 40

    def test_zero_utility_data(self):
        data = UtilityData(monthly_bill_amount=0, payment_timeliness=0, months_of_history=0)
        score = score_utility_data(data)
        assert score == 0

    def test_max_utility_score(self):
        data = UtilityData(monthly_bill_amount=2000, payment_timeliness=1.0, months_of_history=24)
        score = score_utility_data(data)
        assert score == 100.0


# ─── E-commerce Score Tests ─────────────────────────────────────────────────

class TestEcommerceScore:
    def test_high_activity(self):
        data = EcommerceData(purchase_frequency=8, average_order_value=3000,
                            return_rate=0.02, months_active=12)
        score = score_ecommerce_data(data)
        assert score > 80

    def test_low_activity(self):
        data = EcommerceData(purchase_frequency=1, average_order_value=300,
                            return_rate=0.25, months_active=2)
        score = score_ecommerce_data(data)
        assert score < 40

    def test_zero_ecommerce_data(self):
        data = EcommerceData(purchase_frequency=0, average_order_value=0,
                            return_rate=0, months_active=0)
        score = score_ecommerce_data(data)
        # return_rate=0 gives full return points, so score > 0
        assert score >= 0

    def test_high_return_rate_penalty(self):
        low_return = EcommerceData(purchase_frequency=5, average_order_value=2000,
                                  return_rate=0.05, months_active=10)
        high_return = EcommerceData(purchase_frequency=5, average_order_value=2000,
                                   return_rate=0.28, months_active=10)
        assert score_ecommerce_data(low_return) > score_ecommerce_data(high_return)


# ─── Mobility Score Tests ───────────────────────────────────────────────────

class TestMobilityScore:
    def test_vehicle_owner_commercial(self):
        data = MobilityData(vehicle_ownership=True, vehicle_type="commercial",
                           fuel_expense_monthly=3000, months_tracked=24)
        score = score_mobility_data(data)
        assert score > 80

    def test_no_vehicle(self):
        data = MobilityData(vehicle_ownership=False, vehicle_type="none",
                           fuel_expense_monthly=0, months_tracked=0)
        score = score_mobility_data(data)
        assert score == 0

    def test_vehicle_type_comparison(self):
        commercial = MobilityData(vehicle_ownership=True, vehicle_type="commercial",
                                 fuel_expense_monthly=500, months_tracked=12)
        two_wheeler = MobilityData(vehicle_ownership=True, vehicle_type="two_wheeler",
                                  fuel_expense_monthly=500, months_tracked=12)
        assert score_mobility_data(commercial) > score_mobility_data(two_wheeler)


# ─── Risk Category Tests ────────────────────────────────────────────────────

class TestRiskCategory:
    def test_high_risk(self):
        assert categorize_risk(35) == "high"

    def test_medium_risk(self):
        assert categorize_risk(55) == "medium"

    def test_low_risk(self):
        assert categorize_risk(85) == "low"

    def test_boundary_high_medium(self):
        assert categorize_risk(40) == "medium"

    def test_boundary_medium_low(self):
        assert categorize_risk(70) == "low"

    def test_zero_score(self):
        assert categorize_risk(0) == "high"

    def test_perfect_score(self):
        assert categorize_risk(100) == "low"


# ─── Confidence Tests ───────────────────────────────────────────────────────

class TestConfidence:
    def test_all_data_provided(self):
        app = _make_application(
            gst_data={"annual_turnover": 100000, "filing_consistency": 0.5, "months_filed": 6, "business_type": "retail"},
            upi_data={"monthly_transaction_volume": 50000, "transaction_frequency": 10, "average_transaction_size": 5000, "months_active": 6},
            telecom_data={"monthly_recharge_amount": 300, "recharge_consistency": 0.8, "months_of_history": 12},
            utility_data={"monthly_bill_amount": 1000, "payment_timeliness": 0.8, "months_of_history": 12},
            ecommerce_data={"purchase_frequency": 5, "average_order_value": 1500, "return_rate": 0.05, "months_active": 6},
            mobility_data={"vehicle_ownership": True, "vehicle_type": "two_wheeler", "fuel_expense_monthly": 500, "months_tracked": 12},
        )
        confidence = calculate_confidence(app)
        assert confidence == 100.0

    def test_no_data_provided(self):
        app = _make_application()
        confidence = calculate_confidence(app)
        assert confidence == 0.0

    def test_partial_data(self):
        app = _make_application(
            upi_data={"monthly_transaction_volume": 50000, "transaction_frequency": 10, "average_transaction_size": 5000, "months_active": 6},
            telecom_data={"monthly_recharge_amount": 300, "recharge_consistency": 0.8, "months_of_history": 12},
        )
        confidence = calculate_confidence(app)
        assert 0 < confidence < 100


# ─── Weighted Average Tests ─────────────────────────────────────────────────

class TestWeightedAverage:
    def test_all_scores_100(self):
        app = _make_application(
            gst_data={"annual_turnover": 1000000, "filing_consistency": 1.0, "months_filed": 12, "business_type": "retail"},
            upi_data={"monthly_transaction_volume": 200000, "transaction_frequency": 50, "average_transaction_size": 5000, "months_active": 24},
            telecom_data={"monthly_recharge_amount": 500, "recharge_consistency": 1.0, "months_of_history": 24},
            utility_data={"monthly_bill_amount": 2000, "payment_timeliness": 1.0, "months_of_history": 24},
            ecommerce_data={"purchase_frequency": 10, "average_order_value": 3000, "return_rate": 0.01, "months_active": 12},
            mobility_data={"vehicle_ownership": True, "vehicle_type": "commercial", "fuel_expense_monthly": 3000, "months_tracked": 24},
        )
        result = calculate_credit_score(app)
        assert result["overall_risk_score"] == 100.0

    def test_all_scores_0(self):
        app = _make_application()
        result = calculate_credit_score(app)
        assert result["overall_risk_score"] == 0.0

    def test_mixed_scores_weighted(self):
        app = _make_application(
            gst_data={"annual_turnover": 500000, "filing_consistency": 0.95, "months_filed": 12, "business_type": "retail"},
            upi_data={"monthly_transaction_volume": 100000, "transaction_frequency": 25, "average_transaction_size": 4000, "months_active": 18},
        )
        result = calculate_credit_score(app)
        assert 0 < result["overall_risk_score"] < 100
        assert result["gst_score"] > 0
        assert result["upi_score"] > 0

    def test_result_has_all_fields(self):
        app = _make_application()
        result = calculate_credit_score(app)
        assert "overall_risk_score" in result
        assert "risk_category" in result
        assert "gst_score" in result
        assert "upi_score" in result
        assert "telecom_score" in result
        assert "utility_score" in result
        assert "ecommerce_score" in result
        assert "mobility_score" in result
        assert "confidence_level" in result


# ─── Edge Case Tests ────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_unicode_name(self):
        app = _make_application(name="राजेश कुमार")
        result = calculate_credit_score(app)
        assert result is not None

    def test_boundary_values(self):
        """Test with exact threshold values."""
        data = GSTData(annual_turnover=300000, filing_consistency=0.9, months_filed=11, business_type="retail")
        score = score_gst_data(data)
        assert score > 0

    def test_very_large_turnover(self):
        data = GSTData(annual_turnover=10000000, filing_consistency=1.0, months_filed=12, business_type="retail")
        score = score_gst_data(data)
        assert score == 100.0

    def test_score_bounds(self):
        """All scores must be between 0 and 100."""
        app = _make_application(
            gst_data={"annual_turnover": 500000, "filing_consistency": 0.9, "months_filed": 11, "business_type": "retail"},
            upi_data={"monthly_transaction_volume": 120000, "transaction_frequency": 30, "average_transaction_size": 4000, "months_active": 20},
            telecom_data={"monthly_recharge_amount": 350, "recharge_consistency": 0.95, "months_of_history": 24},
            utility_data={"monthly_bill_amount": 1800, "payment_timeliness": 0.88, "months_of_history": 18},
            ecommerce_data={"purchase_frequency": 6, "average_order_value": 2500, "return_rate": 0.04, "months_active": 14},
            mobility_data={"vehicle_ownership": True, "vehicle_type": "two_wheeler", "fuel_expense_monthly": 1000, "months_tracked": 20},
        )
        result = calculate_credit_score(app)
        for key, val in result.items():
            if isinstance(val, float):
                assert 0 <= val <= 100, f"{key} out of bounds: {val}"
