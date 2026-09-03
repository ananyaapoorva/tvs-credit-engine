"""Constants used throughout the credit scoring engine."""

# ─── Component Weights ───────────────────────────────────────────────────────
GST_WEIGHT = 0.20
UPI_WEIGHT = 0.20
TELECOM_WEIGHT = 0.15
UTILITY_WEIGHT = 0.15
ECOMMERCE_WEIGHT = 0.15
MOBILITY_WEIGHT = 0.15

# ─── Risk Category Thresholds ────────────────────────────────────────────────
HIGH_RISK_THRESHOLD = 40
MEDIUM_RISK_THRESHOLD = 70

# ─── GST Scoring Constants ───────────────────────────────────────────────────
GST_HIGH_TURNOVER = 300000           # ₹3L threshold
GST_HIGH_CONSISTENCY = 0.90          # 90% filing consistency
GST_HIGH_MONTHS = 11                 # 11 of 12 months filed
GST_HIGH_RISK_BUSINESS_TYPES = {"liquor", "gambling", "speculative"}
GST_TURNOVER_POINTS = 20
GST_CONSISTENCY_POINTS = 20
GST_FREQUENCY_POINTS = 20
GST_MAX_POINTS = 60
GST_RISK_DEDUCTION = 15

# ─── UPI Scoring Constants ───────────────────────────────────────────────────
UPI_HIGH_VOLUME = 80000              # ₹80K monthly volume
UPI_HIGH_FREQUENCY = 20             # 20 transactions/month
UPI_HIGH_MONTHS = 12                # 12 months active
UPI_AVG_SIZE_THRESHOLD = 2000      # ₹2K average transaction
UPI_VOLUME_POINTS = 25
UPI_FREQUENCY_POINTS = 20
UPI_DURATION_POINTS = 20
UPI_AVG_SIZE_POINTS = 15
UPI_MAX_POINTS = 80

# ─── Telecom Scoring Constants ───────────────────────────────────────────────
TELECOM_HIGH_CONSISTENCY = 0.90      # 90% recharge consistency
TELECOM_MIN_RECHARGE = 200          # ₹200 minimum monthly recharge
TELECOM_HIGH_MONTHS = 12            # 12 months of history
TELECOM_CONSISTENCY_POINTS = 30
TELECOM_AMOUNT_POINTS = 20
TELECOM_HISTORY_POINTS = 25
TELECOM_GAPS_POINTS = 25
TELECOM_MAX_POINTS = 100

# ─── Utility Scoring Constants ───────────────────────────────────────────────
UTILITY_HIGH_TIMELINESS = 0.85       # 85% on-time payment
UTILITY_MIN_BILL = 1000             # ₹1K minimum monthly bill
UTILITY_HIGH_MONTHS = 12            # 12 months of history
UTILITY_TIMELINESS_POINTS = 30
UTILITY_BILL_AMOUNT_POINTS = 20
UTILITY_HISTORY_POINTS = 25
UTILITY_PATTERN_POINTS = 25
UTILITY_MAX_POINTS = 100

# ─── E-commerce Scoring Constants ────────────────────────────────────────────
ECOMMERCE_HIGH_FREQUENCY = 4         # 4 purchases/month
ECOMMERCE_LOW_RETURN_RATE = 0.10    # 10% return rate threshold
ECOMMERCE_HIGH_AOV = 1500           # ₹1.5K average order value
ECOMMERCE_HIGH_MONTHS = 8           # 8 months active
ECOMMERCE_FREQUENCY_POINTS = 20
ECOMMERCE_RETURN_POINTS = 25
ECOMMERCE_AOV_POINTS = 20
ECOMMERCE_DURATION_POINTS = 20
ECOMMERCE_MAX_POINTS = 85

# ─── Mobility Scoring Constants ──────────────────────────────────────────────
MOBILITY_OWNERSHIP_POINTS = 20
MOBILITY_CONSISTENCY_POINTS = 25
MOBILITY_DURATION_POINTS = 25
MOBILITY_TYPE_POINTS = 15
MOBILITY_HIGH_MONTHS = 12           # 12 months tracked
MOBILITY_MIN_FUEL_EXPENSE = 300     # ₹300 minimum fuel expense
MOBILITY_MAX_POINTS = 85

# ─── Vehicle Type Scoring ────────────────────────────────────────────────────
VEHICLE_TYPE_SCORES = {
    "commercial": 15,
    "three_wheeler": 12,
    "car": 10,
    "two_wheeler": 8,
    "none": 0,
}

# ─── Score Bounds ────────────────────────────────────────────────────────────
MIN_SCORE = 0.0
MAX_SCORE = 100.0

# ─── Confidence Calculation ──────────────────────────────────────────────────
TOTAL_DATA_FIELDS = 6  # Number of data source categories
