"""
Tests for the headless CLI and null-data-source robustness.

Covers two shipped fixes:

1. **Null data-source crash (regression):** ``calculate_credit_score`` and
   ``generate_explanation`` used to raise ``AttributeError`` when a credit
   application listed any data source as ``null`` (e.g. an informal-sector
   applicant with no GST or UPI history). Each scorer now returns ``0.0`` for a
   ``None`` source and the explanation generator treats null inputs as "no data".

2. **Headless CLI:** ``tvs-credit`` scores a JSON application file through the
   same services the API uses, emitting either a human-readable report or --
   with ``--json`` -- a pipeable JSON document on stdout.
"""

import json
import sys
from pathlib import Path

import pytest

import cli
from app.schemas.credit_input import CreditApplicationInput
from app.services.explainability import generate_explanation
from app.services.scoring_engine import (
    calculate_confidence,
    calculate_credit_score,
    score_ecommerce_data,
    score_gst_data,
    score_mobility_data,
    score_telecom_data,
    score_upi_data,
    score_utility_data,
)

VALID_BASE = {
    "name": "Test User",
    "phone_number": "9876543210",
    "email": "test@example.com",
    "date_of_birth": "1990-05-15",
    "occupation": "small_merchant",
    "loan_amount_requested": 50000,
}


def _application(**overrides) -> CreditApplicationInput:
    payload = dict(VALID_BASE)
    payload.update(overrides)
    return CreditApplicationInput.model_validate(payload)


# ─── Null data-source robustness ─────────────────────────────────────────────

class TestNullDataSourceScoring:
    @pytest.mark.parametrize(
        "scorer",
        [
            score_gst_data,
            score_upi_data,
            score_telecom_data,
            score_utility_data,
            score_ecommerce_data,
            score_mobility_data,
        ],
        ids=["gst", "upi", "telecom", "utility", "ecommerce", "mobility"],
    )
    def test_each_scorer_accepts_none(self, scorer):
        """Every scorer must return 0.0 for a missing data source, not crash."""
        assert scorer(None) == 0.0

    def test_all_null_sources_calculate_credit_score(self):
        """Scoring with every source null must not raise and must yield 0."""
        scores = calculate_credit_score(_application())
        assert scores["overall_risk_score"] == 0.0
        assert scores["risk_category"] == "high"
        assert scores["confidence_level"] == 0.0
        for key in ("gst_score", "upi_score", "telecom_score", "utility_score",
                    "ecommerce_score", "mobility_score"):
            assert scores[key] == 0.0

    def test_single_null_source_does_not_crash(self):
        """A null Gst source with real UPI data scores contributions separately."""
        app = _application(
            gst_data=None,
            upi_data={
                "monthly_transaction_volume": 90000,
                "transaction_frequency": 25,
                "average_transaction_size": 4000,
                "months_active": 18,
            },
        )
        scores = calculate_credit_score(app)
        assert scores["gst_score"] == 0.0
        assert scores["upi_score"] > 0
        assert scores["overall_risk_score"] > 0

    def test_null_source_same_as_omitted(self):
        """Null and omitted data sources must score identically."""
        null_app = _application(gst_data=None)
        omitted_app = _application()
        assert calculate_credit_score(null_app) == calculate_credit_score(omitted_app)


class TestNullDataSourceExplainability:
    def test_generate_explanation_with_all_null(self):
        """Explanation generation must not raise when all sources are null."""
        app = _application()
        exp = generate_explanation(calculate_credit_score(app), app.model_dump())
        assert len(exp["factors"]) == 6
        assert exp["summary"]
        assert exp["recommendation"]

    def test_null_source_marked_no_data(self):
        """A null Gst source should be explained as 'No GST data provided'."""
        app = _application(gst_data=None, upi_data={
            "monthly_transaction_volume": 90000,
            "transaction_frequency": 25,
            "average_transaction_size": 4000,
            "months_active": 18,
        })
        exp = generate_explanation(calculate_credit_score(app), app.model_dump())
        gst_factor = next(f for f in exp["factors"] if f["category"] == "GST Data")
        assert gst_factor["signal"] == "No GST data provided"
        assert gst_factor["impact"] == "neutral"


# ─── CLI ─────────────────────────────────────────────────────────────────────

class TestCLI:
    def _write_app(self, tmp_path: Path, payload: dict) -> Path:
        path = tmp_path / "app.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def test_version(self, capsys):
        assert cli.main(["--version"]) == 0
        out = capsys.readouterr().out
        assert out.strip() == f"tvs-credit {cli.__version__}"

    def test_missing_file_exits_nonzero(self, capsys):
        assert cli.main(["--json", "/nonexistent/app.json"]) == 1
        err = capsys.readouterr().err
        assert "could not read application file" in err

    def test_no_file_arg_prints_usage(self, capsys):
        assert cli.main([]) == 2
        err = capsys.readouterr().err
        assert "application JSON FILE" in err

    def test_invalid_application_exits_nonzero(self, tmp_path, capsys):
        bad = self._write_app(tmp_path, {"name": "x"})  # missing required fields
        assert cli.main(["--json", str(bad)]) == 1
        err = capsys.readouterr().err
        assert "invalid application data" in err

    def test_underage_exits_nonzero(self, tmp_path, capsys):
        payload = dict(VALID_BASE, date_of_birth="2020-01-01")
        path = self._write_app(tmp_path, payload)
        assert cli.main(["--json", str(path)]) == 1
        err = capsys.readouterr().err
        assert "at least 18" in err

    def test_json_output_is_valid_and_complete(self, tmp_path, capsys):
        payload = {
            **VALID_BASE,
            "gst_data": {"annual_turnover": 450000, "filing_consistency": 0.92,
                         "months_filed": 11, "business_type": "retail"},
            "upi_data": {"monthly_transaction_volume": 95000,
                         "transaction_frequency": 22,
                         "average_transaction_size": 4318, "months_active": 18},
        }
        path = self._write_app(tmp_path, payload)
        assert cli.main(["--json", str(path)]) == 0
        out = capsys.readouterr().out
        report = json.loads(out)
        assert "overall_risk_score" in report
        assert report["risk_category"] in ("low", "medium", "high")
        assert set(report["component_scores"]) == {
            "gst_score", "upi_score", "telecom_score",
            "utility_score", "ecommerce_score", "mobility_score",
        }
        assert len(report["factors"]) == 6
        assert report["summary"]
        assert report["recommendation"]

    def test_json_output_gst_null(self, tmp_path, capsys):
        """Null sources should score as 0 with a valid JSON report (no crash)."""
        payload = {**VALID_BASE, "gst_data": None}
        path = self._write_app(tmp_path, payload)
        assert cli.main(["--json", str(path)]) == 0
        out = capsys.readouterr().out
        report = json.loads(out)
        assert report["component_scores"]["gst_score"] == 0.0
        assert report["overall_risk_score"] == 0.0

    def test_human_output_contains_summary(self, tmp_path, capsys):
        path = self._write_app(tmp_path, dict(VALID_BASE))
        assert cli.main([str(path)]) == 0
        out = capsys.readouterr().out
        assert "Overall risk score" in out
        assert "Recommendation" in out

    def test_null_source_matches_api_scores(self, tmp_path, capsys):
        """CLI must produce identical numbers to the in-process scorer."""
        payload = dict(VALID_BASE, gst_data=None)
        path = self._write_app(tmp_path, payload)
        assert cli.main(["--json", str(path)]) == 0
        report = json.loads(capsys.readouterr().out)

        app = _application(gst_data=None)
        assert calculate_confidence(app) == report["confidence_level"]
        assert float(calculate_credit_score(app)["overall_risk_score"]) == report[
            "overall_risk_score"
        ]