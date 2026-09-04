# API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

All endpoints are prefixed with `/api/v1`. The auto-generated interactive Swagger documentation is available at `http://localhost:8000/docs`.

---

## Endpoints

### Health Check

```
GET /health
```

Returns the current health status of the API.

**Response (200):**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected"
}
```

---

### Submit Credit Application

```
POST /credit/score
```

Submit a credit application with alternative data and receive a risk score with explainability.

**Request Body:**
```json
{
  "name": "Rajesh Kumar",
  "phone_number": "9876543210",
  "email": "rajesh@example.com",
  "date_of_birth": "1990-05-15",
  "occupation": "small_merchant",
  "loan_amount_requested": 50000,
  "gst_data": {
    "annual_turnover": 500000,
    "filing_consistency": 0.9,
    "months_filed": 11,
    "business_type": "retail"
  },
  "upi_data": {
    "monthly_transaction_volume": 100000,
    "transaction_frequency": 25,
    "average_transaction_size": 4000,
    "months_active": 18
  },
  "telecom_data": {
    "monthly_recharge_amount": 300,
    "recharge_consistency": 0.95,
    "months_of_history": 24
  },
  "utility_data": {
    "monthly_bill_amount": 1500,
    "payment_timeliness": 0.85,
    "months_of_history": 12
  },
  "ecommerce_data": {
    "purchase_frequency": 5,
    "average_order_value": 2000,
    "return_rate": 0.05,
    "months_active": 12
  },
  "mobility_data": {
    "vehicle_ownership": true,
    "vehicle_type": "two_wheeler",
    "fuel_expense_monthly": 500,
    "months_tracked": 24
  }
}
```

**Response (200):**
```json
{
  "score_id": "uuid",
  "customer_id": "uuid",
  "overall_risk_score": 72.5,
  "risk_category": "medium",
  "component_scores": {
    "gst_score": 85.0,
    "upi_score": 78.0,
    "telecom_score": 92.0,
    "utility_score": 70.0,
    "ecommerce_score": 68.0,
    "mobility_score": 75.0
  },
  "confidence_level": 82.5,
  "explainability": {
    "factors": [
      {
        "category": "UPI Transactions",
        "signal": "Strong monthly transaction volume",
        "impact": "positive",
        "contribution": "+20 points",
        "explanation": "Regular UPI activity demonstrates active digital financial participation"
      }
    ],
    "summary": "Application shows strong income generation and payment discipline.",
    "recommendation": "Loan approval recommended with standard terms."
  },
  "generated_at": "2025-01-15T10:30:00Z"
}
```

**Error Response (400):**
```json
{
  "detail": "Applicant must be at least 18 years old"
}
```

**Error Response (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "phone_number"],
      "msg": "Invalid Indian phone number format",
      "type": "value_error"
    }
  ]
}
```

---

### Retrieve Credit Score

```
GET /credit/score/{score_id}
```

Retrieve a previously calculated credit score by its unique ID.

**Path Parameters:**
- `score_id` (string, required): The UUID of the score record.

**Response (200):** Same as the POST /credit/score response.

**Error Response (404):**
```json
{
  "detail": "Score not found"
}
```

---

### Get Customer Scores

```
GET /credit/customer/{customer_id}/scores
```

List all scores for a given customer, ordered by most recent first.

**Path Parameters:**
- `customer_id` (string, required): The UUID of the customer.

**Response (200):**
```json
{
  "customer_id": "uuid",
  "customer_name": "Rajesh Kumar",
  "scores": [
    {
      "score_id": "uuid",
      "overall_risk_score": 72.5,
      "risk_category": "medium",
      "confidence_level": 82.5,
      "generated_at": "2025-01-15T10:30:00Z"
    }
  ],
  "total_count": 1
}
```

---

### List Recent Customers

```
GET /credit/customers
```

Fetch the 20 most recently scored customers for the comparison feature.

**Response (200):**
```json
[
  {
    "customer_id": "uuid",
    "name": "Rajesh Kumar",
    "phone_number": "9876543210",
    "occupation": "small_merchant",
    "created_at": "2025-01-15T10:30:00Z"
  }
]
```

---

### Compare Customers

```
POST /credit/compare?customer_id_1={id}&customer_id_2={id}
```

Compare the most recent risk profiles of two customers side-by-side.

**Query Parameters:**
- `customer_id_1` (string, required): UUID of the first customer.
- `customer_id_2` (string, required): UUID of the second customer.

**Response (200):**
```json
{
  "customer_1": { "...full CreditScoreOutput..." },
  "customer_2": { "...full CreditScoreOutput..." }
}
```

---

### Mock Customers

```
GET /credit/mock-customers
```

Returns all 10 predefined mock customer profiles for demo and testing purposes.

```
GET /credit/mock-customers/{index}
```

Returns a single mock customer by index (0-9).
