# Alternative Credit Scoring Algorithm

## Overview

This document explains how the TVS Credit Alternative Data Credit Engine calculates risk scores using 6 alternative data sources. The engine is entirely **deterministic and rule-based** -- it uses no machine learning models. This design was chosen to maximize **explainability**, which is critical for regulatory compliance and building trust with underserved borrowers.

## Why Alternative Data?

Traditional credit scoring (CIBIL) requires a formal banking history, which excludes:
- **First-time borrowers** with no credit file
- **Gig workers** (delivery drivers, freelancers) with irregular income
- **Small merchants** operating in cash-heavy economies
- **Informal sector workers** without formal employment contracts

Alternative data captures the digital footprint these individuals already generate -- GST filings, UPI transactions, phone recharges, utility bills, online purchases, and vehicle usage -- to build a proxy for creditworthiness.

---

## Data Sources and Weights

| Data Source | Weight | Rationale |
|---|---|---|
| GST Data | 20% | Formal business activity is a strong income signal |
| UPI Transactions | 20% | Real-time cash flow reflects actual earning capacity |
| Telecom Recharge | 15% | Consistent recharges indicate financial discipline |
| Utility Payments | 15% | On-time bill payments predict loan repayment behavior |
| E-commerce Activity | 15% | Purchase patterns reveal disposable income stability |
| Mobility/Vehicle | 15% | Vehicle ownership and fuel usage indicate asset base |

If a data source is entirely missing (all fields zero), the engine dynamically redistributes its weight proportionally across the remaining sources.

---

## Scoring Logic Per Component

### GST Score (0-100)

| Signal | Points | Threshold |
|---|---|---|
| Annual Turnover | 20 | >= 3,00,000 (proportional below) |
| Filing Consistency | 20 | >= 90% (proportional below) |
| Months Filed | 20 | >= 11 of 12 (proportional below) |
| High-Risk Business Type | -15 | liquor, gambling, speculative |

**Max Raw Points:** 60
**Normalization:** `(raw_points / 60) * 100`

### UPI Score (0-100)

| Signal | Points | Threshold |
|---|---|---|
| Monthly Transaction Volume | 25 | >= 80,000 (proportional below) |
| Transaction Frequency | 20 | >= 20/month (proportional below) |
| Months Active | 20 | >= 12 months (proportional below) |
| Average Transaction Size | 15 | >= 2,000 (proportional below) |

**Max Raw Points:** 80
**Normalization:** `(raw_points / 80) * 100`

### Telecom Score (0-100)

| Signal | Points | Threshold |
|---|---|---|
| Recharge Consistency | 30 | >= 90% (proportional below) |
| Monthly Recharge Amount | 20 | >= 200 (proportional below) |
| Months of History | 25 | >= 12 months (proportional below) |
| No Service Gaps | 25 | Derived from consistency >= 90% |

**Max Raw Points:** 100
**Normalization:** `(raw_points / 100) * 100`

### Utility Score (0-100)

| Signal | Points | Threshold |
|---|---|---|
| Payment Timeliness | 30 | >= 85% on-time (proportional below) |
| Monthly Bill Amount | 20 | >= 1,000 (proportional below) |
| Months of History | 25 | >= 12 months (proportional below) |
| Regular Payment Pattern | 25 | Timeliness >= 85% AND history >= 12 months |

**Max Raw Points:** 100
**Normalization:** `(raw_points / 100) * 100`

### E-commerce Score (0-100)

| Signal | Points | Threshold |
|---|---|---|
| Purchase Frequency | 20 | >= 4/month (proportional below) |
| Low Return Rate | 25 | <= 10% (scaled penalty up to 30%) |
| Average Order Value | 20 | >= 1,500 (proportional below) |
| Months Active | 20 | >= 8 months (proportional below) |

**Max Raw Points:** 85
**Normalization:** `(raw_points / 85) * 100`

### Mobility Score (0-100)

| Signal | Points | Threshold |
|---|---|---|
| Vehicle Ownership | 20 | Boolean |
| Fuel Expense Consistency | 25 | >= 300/month (proportional below) |
| Months Tracked | 25 | >= 12 months (proportional below) |
| Vehicle Type | 15 | commercial=15, three_wheeler=12, car=10, two_wheeler=8 |

**Max Raw Points:** 85
**Normalization:** `(raw_points / 85) * 100`

---

## Overall Risk Score

```
Overall = (GST * 0.20) + (UPI * 0.20) + (Telecom * 0.15) + (Utility * 0.15) + (E-commerce * 0.15) + (Mobility * 0.15)
```

All scores are clamped to the range [0, 100].

---

## Risk Categories

| Score Range | Category | Recommendation |
|---|---|---|
| 0-39 | HIGH RISK | Recommend rejection or high interest rate with collateral |
| 40-69 | MEDIUM RISK | Recommend approval with monitoring and standard terms |
| 70-100 | LOW RISK | Recommend approval at lower interest rates |

---

## Confidence Level

Confidence is calculated as the percentage of data sources that contain meaningful (non-zero) data:

```
Confidence = (sources_with_data / 6) * 100
```

A confidence of 100% means all 6 data sources were provided. A confidence of 33% means only 2 of 6 sources had data.

---

## Worked Example: Rajesh Kumar (Small Merchant)

**Input:**
- GST: Turnover 4.5L, 92% consistency, 11 months filed, retail
- UPI: 95K/month volume, 30 txns/month, 3800 avg, 18 months
- Telecom: 350/month recharge, 95% consistency, 24 months
- Utility: 2000/month bill, 88% timeliness, 18 months
- E-commerce: 6 purchases/month, 2500 AOV, 3% returns, 12 months
- Mobility: Owns two-wheeler, 600/month fuel, 24 months tracked

**Component Scores:**
- GST: 20 + 20 + 20 = 60/60 -> **100.0**
- UPI: 25 + 20 + 20 + 15 = 80/80 -> **100.0**
- Telecom: 30 + 20 + 25 + 25 = 100/100 -> **100.0**
- Utility: 30 + 20 + 25 + 25 = 100/100 -> **100.0**
- E-commerce: 20 + 25 + 20 + 20 = 85/85 -> **100.0**
- Mobility: 20 + 25 + 25 + 8 = 78/85 -> **91.8**

**Overall:** (100*0.20) + (100*0.20) + (100*0.15) + (100*0.15) + (100*0.15) + (91.8*0.15) = **98.8**

**Risk Category:** LOW RISK
**Confidence:** 100% (all 6 sources provided)
**Recommendation:** Loan approval recommended at lower interest rates.
