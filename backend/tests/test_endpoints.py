"""
API endpoint integration tests.

Tests all routes with valid/invalid inputs, error handling,
and response format validation.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, engine


@pytest.fixture(autouse=True)
def setup_database():
    """Create tables before each test, drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)

VALID_APPLICATION = {
    "name": "Test User",
    "phone_number": "9876543210",
    "email": "test@example.com",
    "date_of_birth": "1990-05-15",
    "occupation": "small_merchant",
    "loan_amount_requested": 50000,
    "gst_data": {
        "annual_turnover": 450000,
        "filing_consistency": 0.92,
        "months_filed": 11,
        "business_type": "retail"
    },
    "upi_data": {
        "monthly_transaction_volume": 95000,
        "transaction_frequency": 22,
        "average_transaction_size": 4318,
        "months_active": 18
    },
    "telecom_data": {
        "monthly_recharge_amount": 349,
        "recharge_consistency": 0.95,
        "months_of_history": 24
    },
    "utility_data": {
        "monthly_bill_amount": 1800,
        "payment_timeliness": 0.88,
        "months_of_history": 20
    },
    "ecommerce_data": {
        "purchase_frequency": 5,
        "average_order_value": 2200,
        "return_rate": 0.05,
        "months_active": 14
    },
    "mobility_data": {
        "vehicle_ownership": True,
        "vehicle_type": "two_wheeler",
        "fuel_expense_monthly": 1200,
        "months_tracked": 24
    }
}


class TestHealthEndpoint:
    def test_health_check(self):
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "1.0.0"


class TestCreateCreditScore:
    def test_valid_application(self):
        response = client.post("/api/v1/credit/score", json=VALID_APPLICATION)
        assert response.status_code == 200
        data = response.json()
        assert "score_id" in data
        assert "customer_id" in data
        assert 0 <= data["overall_risk_score"] <= 100
        assert data["risk_category"] in ["low", "medium", "high"]
        assert "component_scores" in data
        assert "explainability" in data

    def test_valid_application_response_format(self):
        response = client.post("/api/v1/credit/score", json=VALID_APPLICATION)
        data = response.json()
        cs = data["component_scores"]
        assert "gst_score" in cs
        assert "upi_score" in cs
        assert "telecom_score" in cs
        assert "utility_score" in cs
        assert "ecommerce_score" in cs
        assert "mobility_score" in cs

    def test_explainability_present(self):
        response = client.post("/api/v1/credit/score", json=VALID_APPLICATION)
        data = response.json()
        expl = data["explainability"]
        assert "factors" in expl
        assert "summary" in expl
        assert "recommendation" in expl
        assert len(expl["factors"]) > 0

    def test_minimal_data(self):
        minimal = {
            "name": "Minimal User",
            "phone_number": "9876543211",
            "email": "minimal@example.com",
            "date_of_birth": "1990-01-01",
            "occupation": "other",
            "loan_amount_requested": 10000,
        }
        response = client.post("/api/v1/credit/score", json=minimal)
        assert response.status_code == 200
        data = response.json()
        assert data["overall_risk_score"] == 0
        assert data["risk_category"] == "high"

    def test_invalid_phone_number(self):
        invalid = VALID_APPLICATION.copy()
        invalid["phone_number"] = "12345"
        invalid["email"] = "invalid_phone@example.com"
        response = client.post("/api/v1/credit/score", json=invalid)
        assert response.status_code == 422

    def test_invalid_email(self):
        invalid = VALID_APPLICATION.copy()
        invalid["email"] = "not-an-email"
        invalid["phone_number"] = "9876543299"
        response = client.post("/api/v1/credit/score", json=invalid)
        assert response.status_code == 422

    def test_invalid_occupation(self):
        invalid = VALID_APPLICATION.copy()
        invalid["occupation"] = "astronaut"
        invalid["phone_number"] = "9876543298"
        invalid["email"] = "astronaut@example.com"
        response = client.post("/api/v1/credit/score", json=invalid)
        assert response.status_code == 422

    def test_negative_loan_amount(self):
        invalid = VALID_APPLICATION.copy()
        invalid["loan_amount_requested"] = -5000
        invalid["phone_number"] = "9876543297"
        invalid["email"] = "negative@example.com"
        response = client.post("/api/v1/credit/score", json=invalid)
        assert response.status_code == 422

    def test_underage_applicant(self):
        underage = VALID_APPLICATION.copy()
        underage["date_of_birth"] = "2020-01-01"
        underage["phone_number"] = "9876543296"
        underage["email"] = "underage@example.com"
        response = client.post("/api/v1/credit/score", json=underage)
        assert response.status_code == 400

    def test_duplicate_phone_updates_customer(self):
        # First submission
        response1 = client.post("/api/v1/credit/score", json=VALID_APPLICATION)
        assert response1.status_code == 200
        cust1 = response1.json()["customer_id"]

        # Second submission with same phone
        updated = VALID_APPLICATION.copy()
        updated["name"] = "Updated Name"
        response2 = client.post("/api/v1/credit/score", json=updated)
        assert response2.status_code == 200
        cust2 = response2.json()["customer_id"]
        assert cust1 == cust2  # Same customer


class TestGetCreditScore:
    def test_retrieve_existing_score(self):
        # Create a score first
        create_resp = client.post("/api/v1/credit/score", json=VALID_APPLICATION)
        score_id = create_resp.json()["score_id"]

        # Retrieve it
        response = client.get(f"/api/v1/credit/score/{score_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["score_id"] == score_id

    def test_score_not_found(self):
        response = client.get("/api/v1/credit/score/nonexistent-id")
        assert response.status_code == 404


class TestGetCustomerScores:
    def test_customer_scores(self):
        # Create a score first
        create_resp = client.post("/api/v1/credit/score", json=VALID_APPLICATION)
        customer_id = create_resp.json()["customer_id"]

        response = client.get(f"/api/v1/credit/customer/{customer_id}/scores")
        assert response.status_code == 200
        data = response.json()
        assert data["customer_id"] == customer_id
        assert data["total_count"] >= 1
        assert len(data["scores"]) >= 1

    def test_customer_not_found(self):
        response = client.get("/api/v1/credit/customer/nonexistent-id/scores")
        assert response.status_code == 404


class TestCompareEndpoint:
    def test_compare_two_customers(self):
        # Create two different customers
        app1 = VALID_APPLICATION.copy()
        app2 = VALID_APPLICATION.copy()
        app2["phone_number"] = "8765432100"
        app2["email"] = "compare2@example.com"
        app2["name"] = "Second User"

        resp1 = client.post("/api/v1/credit/score", json=app1)
        resp2 = client.post("/api/v1/credit/score", json=app2)

        cid1 = resp1.json()["customer_id"]
        cid2 = resp2.json()["customer_id"]

        response = client.post(
            f"/api/v1/credit/compare?customer_id_1={cid1}&customer_id_2={cid2}"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["customer_1"] is not None
        assert data["customer_2"] is not None

    def test_compare_nonexistent(self):
        response = client.post(
            "/api/v1/credit/compare?customer_id_1=none1&customer_id_2=none2"
        )
        assert response.status_code == 404


class TestMockCustomers:
    def test_list_mock_customers(self):
        response = client.get("/api/v1/credit/mock-customers")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 10

    def test_get_mock_customer_by_index(self):
        response = client.get("/api/v1/credit/mock-customers/0")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Rajesh Kumar"

    def test_mock_customer_invalid_index(self):
        response = client.get("/api/v1/credit/mock-customers/99")
        assert response.status_code == 404
