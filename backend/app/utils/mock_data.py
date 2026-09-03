"""
Mock data generator with 10 diverse customer profiles.

Covers all occupation types: gig workers, small merchants,
informal sector workers, and first-time borrowers.
"""

import random

from faker import Faker

fake = Faker("en_IN")

MOCK_CUSTOMERS = [
    {
        "name": "Rajesh Kumar",
        "phone_number": "9876543210",
        "email": "rajesh.kumar@example.com",
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
    },
    {
        "name": "Priya Sharma",
        "phone_number": "8765432109",
        "email": "priya.sharma@example.com",
        "date_of_birth": "1995-08-22",
        "occupation": "gig_worker",
        "loan_amount_requested": 25000,
        "gst_data": {
            "annual_turnover": 0,
            "filing_consistency": 0,
            "months_filed": 0,
            "business_type": "other"
        },
        "upi_data": {
            "monthly_transaction_volume": 120000,
            "transaction_frequency": 35,
            "average_transaction_size": 3428,
            "months_active": 24
        },
        "telecom_data": {
            "monthly_recharge_amount": 299,
            "recharge_consistency": 0.97,
            "months_of_history": 30
        },
        "utility_data": {
            "monthly_bill_amount": 1200,
            "payment_timeliness": 0.92,
            "months_of_history": 18
        },
        "ecommerce_data": {
            "purchase_frequency": 8,
            "average_order_value": 1500,
            "return_rate": 0.08,
            "months_active": 20
        },
        "mobility_data": {
            "vehicle_ownership": True,
            "vehicle_type": "two_wheeler",
            "fuel_expense_monthly": 800,
            "months_tracked": 18
        }
    },
    {
        "name": "Mohammed Irfan",
        "phone_number": "7654321098",
        "email": "mohammed.irfan@example.com",
        "date_of_birth": "1985-12-10",
        "occupation": "small_merchant",
        "loan_amount_requested": 200000,
        "gst_data": {
            "annual_turnover": 800000,
            "filing_consistency": 0.98,
            "months_filed": 12,
            "business_type": "wholesale"
        },
        "upi_data": {
            "monthly_transaction_volume": 250000,
            "transaction_frequency": 50,
            "average_transaction_size": 5000,
            "months_active": 36
        },
        "telecom_data": {
            "monthly_recharge_amount": 499,
            "recharge_consistency": 0.99,
            "months_of_history": 48
        },
        "utility_data": {
            "monthly_bill_amount": 3500,
            "payment_timeliness": 0.95,
            "months_of_history": 36
        },
        "ecommerce_data": {
            "purchase_frequency": 3,
            "average_order_value": 5000,
            "return_rate": 0.02,
            "months_active": 24
        },
        "mobility_data": {
            "vehicle_ownership": True,
            "vehicle_type": "commercial",
            "fuel_expense_monthly": 3500,
            "months_tracked": 36
        }
    },
    {
        "name": "Lakshmi Devi",
        "phone_number": "6543210987",
        "email": "lakshmi.devi@example.com",
        "date_of_birth": "1988-03-28",
        "occupation": "informal_sector",
        "loan_amount_requested": 15000,
        "gst_data": {
            "annual_turnover": 0,
            "filing_consistency": 0,
            "months_filed": 0,
            "business_type": "other"
        },
        "upi_data": {
            "monthly_transaction_volume": 35000,
            "transaction_frequency": 12,
            "average_transaction_size": 2916,
            "months_active": 10
        },
        "telecom_data": {
            "monthly_recharge_amount": 199,
            "recharge_consistency": 0.80,
            "months_of_history": 18
        },
        "utility_data": {
            "monthly_bill_amount": 800,
            "payment_timeliness": 0.65,
            "months_of_history": 12
        },
        "ecommerce_data": {
            "purchase_frequency": 2,
            "average_order_value": 800,
            "return_rate": 0.15,
            "months_active": 6
        },
        "mobility_data": {
            "vehicle_ownership": False,
            "vehicle_type": "none",
            "fuel_expense_monthly": 0,
            "months_tracked": 0
        }
    },
    {
        "name": "Arjun Patel",
        "phone_number": "9988776655",
        "email": "arjun.patel@example.com",
        "date_of_birth": "2000-01-05",
        "occupation": "first_time_borrower",
        "loan_amount_requested": 30000,
        "gst_data": {
            "annual_turnover": 0,
            "filing_consistency": 0,
            "months_filed": 0,
            "business_type": "other"
        },
        "upi_data": {
            "monthly_transaction_volume": 45000,
            "transaction_frequency": 18,
            "average_transaction_size": 2500,
            "months_active": 8
        },
        "telecom_data": {
            "monthly_recharge_amount": 399,
            "recharge_consistency": 0.88,
            "months_of_history": 12
        },
        "utility_data": {
            "monthly_bill_amount": 600,
            "payment_timeliness": 0.75,
            "months_of_history": 6
        },
        "ecommerce_data": {
            "purchase_frequency": 6,
            "average_order_value": 1800,
            "return_rate": 0.12,
            "months_active": 10
        },
        "mobility_data": {
            "vehicle_ownership": False,
            "vehicle_type": "none",
            "fuel_expense_monthly": 0,
            "months_tracked": 0
        }
    },
    {
        "name": "Deepa Nair",
        "phone_number": "8877665544",
        "email": "deepa.nair@example.com",
        "date_of_birth": "1992-07-18",
        "occupation": "gig_worker",
        "loan_amount_requested": 75000,
        "gst_data": {
            "annual_turnover": 180000,
            "filing_consistency": 0.60,
            "months_filed": 7,
            "business_type": "service"
        },
        "upi_data": {
            "monthly_transaction_volume": 85000,
            "transaction_frequency": 28,
            "average_transaction_size": 3035,
            "months_active": 20
        },
        "telecom_data": {
            "monthly_recharge_amount": 249,
            "recharge_consistency": 0.92,
            "months_of_history": 24
        },
        "utility_data": {
            "monthly_bill_amount": 1400,
            "payment_timeliness": 0.82,
            "months_of_history": 14
        },
        "ecommerce_data": {
            "purchase_frequency": 4,
            "average_order_value": 2500,
            "return_rate": 0.06,
            "months_active": 16
        },
        "mobility_data": {
            "vehicle_ownership": True,
            "vehicle_type": "two_wheeler",
            "fuel_expense_monthly": 600,
            "months_tracked": 12
        }
    },
    {
        "name": "Suresh Yadav",
        "phone_number": "7766554433",
        "email": "suresh.yadav@example.com",
        "date_of_birth": "1982-11-30",
        "occupation": "small_merchant",
        "loan_amount_requested": 100000,
        "gst_data": {
            "annual_turnover": 650000,
            "filing_consistency": 0.85,
            "months_filed": 10,
            "business_type": "manufacturing"
        },
        "upi_data": {
            "monthly_transaction_volume": 180000,
            "transaction_frequency": 40,
            "average_transaction_size": 4500,
            "months_active": 30
        },
        "telecom_data": {
            "monthly_recharge_amount": 599,
            "recharge_consistency": 0.90,
            "months_of_history": 36
        },
        "utility_data": {
            "monthly_bill_amount": 2800,
            "payment_timeliness": 0.90,
            "months_of_history": 30
        },
        "ecommerce_data": {
            "purchase_frequency": 2,
            "average_order_value": 4000,
            "return_rate": 0.03,
            "months_active": 18
        },
        "mobility_data": {
            "vehicle_ownership": True,
            "vehicle_type": "three_wheeler",
            "fuel_expense_monthly": 2000,
            "months_tracked": 24
        }
    },
    {
        "name": "Anjali Gupta",
        "phone_number": "6655443322",
        "email": "anjali.gupta@example.com",
        "date_of_birth": "1998-04-12",
        "occupation": "gig_worker",
        "loan_amount_requested": 20000,
        "gst_data": {
            "annual_turnover": 0,
            "filing_consistency": 0,
            "months_filed": 0,
            "business_type": "other"
        },
        "upi_data": {
            "monthly_transaction_volume": 60000,
            "transaction_frequency": 20,
            "average_transaction_size": 3000,
            "months_active": 14
        },
        "telecom_data": {
            "monthly_recharge_amount": 199,
            "recharge_consistency": 0.85,
            "months_of_history": 14
        },
        "utility_data": {
            "monthly_bill_amount": 900,
            "payment_timeliness": 0.78,
            "months_of_history": 10
        },
        "ecommerce_data": {
            "purchase_frequency": 7,
            "average_order_value": 1200,
            "return_rate": 0.10,
            "months_active": 12
        },
        "mobility_data": {
            "vehicle_ownership": False,
            "vehicle_type": "none",
            "fuel_expense_monthly": 0,
            "months_tracked": 0
        }
    },
    {
        "name": "Vikram Singh",
        "phone_number": "9944332211",
        "email": "vikram.singh@example.com",
        "date_of_birth": "1978-09-25",
        "occupation": "informal_sector",
        "loan_amount_requested": 40000,
        "gst_data": {
            "annual_turnover": 120000,
            "filing_consistency": 0.40,
            "months_filed": 4,
            "business_type": "retail"
        },
        "upi_data": {
            "monthly_transaction_volume": 25000,
            "transaction_frequency": 8,
            "average_transaction_size": 3125,
            "months_active": 6
        },
        "telecom_data": {
            "monthly_recharge_amount": 149,
            "recharge_consistency": 0.70,
            "months_of_history": 36
        },
        "utility_data": {
            "monthly_bill_amount": 1100,
            "payment_timeliness": 0.60,
            "months_of_history": 24
        },
        "ecommerce_data": {
            "purchase_frequency": 1,
            "average_order_value": 900,
            "return_rate": 0.20,
            "months_active": 4
        },
        "mobility_data": {
            "vehicle_ownership": True,
            "vehicle_type": "two_wheeler",
            "fuel_expense_monthly": 400,
            "months_tracked": 12
        }
    },
    {
        "name": "Meena Kumari",
        "phone_number": "8833221100",
        "email": "meena.kumari@example.com",
        "date_of_birth": "1993-06-08",
        "occupation": "first_time_borrower",
        "loan_amount_requested": 10000,
        "gst_data": {
            "annual_turnover": 0,
            "filing_consistency": 0,
            "months_filed": 0,
            "business_type": "other"
        },
        "upi_data": {
            "monthly_transaction_volume": 15000,
            "transaction_frequency": 5,
            "average_transaction_size": 3000,
            "months_active": 4
        },
        "telecom_data": {
            "monthly_recharge_amount": 149,
            "recharge_consistency": 0.75,
            "months_of_history": 8
        },
        "utility_data": {
            "monthly_bill_amount": 500,
            "payment_timeliness": 0.50,
            "months_of_history": 6
        },
        "ecommerce_data": {
            "purchase_frequency": 1,
            "average_order_value": 600,
            "return_rate": 0.25,
            "months_active": 3
        },
        "mobility_data": {
            "vehicle_ownership": False,
            "vehicle_type": "none",
            "fuel_expense_monthly": 0,
            "months_tracked": 0
        }
    },
]


def get_mock_customer(index: int) -> dict:
    """Get a mock customer by index (0-9)."""
    if 0 <= index < len(MOCK_CUSTOMERS):
        return MOCK_CUSTOMERS[index]
    raise IndexError(f"Mock customer index must be 0-{len(MOCK_CUSTOMERS) - 1}")


def get_all_mock_customers() -> list:
    """Return all mock customer profiles."""
    return MOCK_CUSTOMERS


def generate_random_customer() -> dict:
    """Generate a random customer profile using Faker."""
    return {
        "name": fake.name(),
        "phone_number": f"{random.choice(['6','7','8','9'])}{random.randint(100000000, 999999999)}",
        "email": fake.email(),
        "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=65).isoformat(),
        "occupation": random.choice([
            "gig_worker", "small_merchant", "informal_sector",
            "first_time_borrower", "other"
        ]),
        "loan_amount_requested": random.choice([
            10000, 25000, 50000, 75000, 100000, 200000
        ]),
        "gst_data": {
            "annual_turnover": random.choice([0, 100000, 300000, 500000, 800000]),
            "filing_consistency": round(random.uniform(0, 1), 2),
            "months_filed": random.randint(0, 12),
            "business_type": random.choice(["retail", "wholesale", "service", "manufacturing", "other"])
        },
        "upi_data": {
            "monthly_transaction_volume": random.randint(5000, 300000),
            "transaction_frequency": random.randint(2, 60),
            "average_transaction_size": random.randint(500, 10000),
            "months_active": random.randint(1, 36)
        },
        "telecom_data": {
            "monthly_recharge_amount": random.choice([149, 199, 249, 299, 349, 399, 499, 599]),
            "recharge_consistency": round(random.uniform(0.5, 1.0), 2),
            "months_of_history": random.randint(3, 48)
        },
        "utility_data": {
            "monthly_bill_amount": random.randint(300, 5000),
            "payment_timeliness": round(random.uniform(0.4, 1.0), 2),
            "months_of_history": random.randint(3, 36)
        },
        "ecommerce_data": {
            "purchase_frequency": random.randint(0, 15),
            "average_order_value": random.randint(300, 8000),
            "return_rate": round(random.uniform(0, 0.3), 2),
            "months_active": random.randint(1, 24)
        },
        "mobility_data": {
            "vehicle_ownership": random.choice([True, False]),
            "vehicle_type": random.choice(["two_wheeler", "three_wheeler", "car", "commercial", "none"]),
            "fuel_expense_monthly": random.randint(0, 5000),
            "months_tracked": random.randint(0, 36)
        },
    }
