"""
Headless command-line interface for the TVS Credit scoring engine.

Provides a scriptable path to the same deterministic, explainable scoring
logic exposed by the FastAPI ``/api/v1/credit/score`` endpoint, so lending
pipelines and batch jobs can score alternative-data applications without
running a web server or database.

The CLI reuses the exact service modules the API uses (``CreditApplicationInput``
validation, ``validate_application_data`` business rules, ``calculate_credit_score``
and ``generate_explanation``), so scores never diverge between the two paths.
"""

from __future__ import annotations

import argparse
import json
import sys

from app.schemas.credit_input import CreditApplicationInput
from app.services.data_validator import validate_application_data
from app.services.explainability import generate_explanation
from app.services.scoring_engine import calculate_credit_score

__version__ = "1.1.0"

SOURCE_LABELS = {
    "gst_score": "GST filing & turnover",
    "upi_score": "UPI transactions",
    "telecom_score": "Telecom recharge",
    "utility_score": "Utility bills",
    "ecommerce_score": "E-commerce activity",
    "mobility_score": "Mobility & vehicle",
}


def _load_application(path: str) -> dict:
    """Read and parse a credit application JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("Application JSON must be an object")
    return data


def _build_report(scores: dict, explanation: dict) -> dict:
    """Assemble the full machine-readable assessment payload."""
    return {
        "overall_risk_score": scores["overall_risk_score"],
        "risk_category": scores["risk_category"],
        "confidence_level": scores["confidence_level"],
        "component_scores": {
            k: scores[k]
            for k in SOURCE_LABELS
        },
        "factors": explanation["factors"],
        "summary": explanation["summary"],
        "recommendation": explanation["recommendation"],
    }


def _render_human(report: dict) -> str:
    """Render a report dict as a human-readable text summary."""
    lines = [
        "TVS Credit — Alternative Data Credit Assessment",
        "=" * 48,
        f"Overall risk score : {report['overall_risk_score']:.1f}/100  ({report['risk_category'].upper()} RISK)",
        f"Confidence level   : {report['confidence_level']:.1f}%",
        "",
        "Component scores:",
    ]
    for key, label in SOURCE_LABELS.items():
        lines.append(f"  {label:<28} {report['component_scores'][key]:6.1f}")
    lines.append("")
    lines.append(f"Summary        : {report['summary']}")
    lines.append(f"Recommendation : {report['recommendation']}")
    lines.append("")
    lines.append("Factors:")
    for f in report["factors"]:
        lines.append(
            f"  [{f['impact']:<8}] {f['category']} — {f['signal']} "
            f"({f['contribution']})"
        )
    lines.append("")
    lines.append("Note: scores are deterministic, rule-based, and fully explainable.")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="tvs-credit",
        description=(
            "Score an alternative-data credit application using the TVS Credit "
            "engine's deterministic, explainable rule-based model."
        ),
    )
    parser.add_argument(
        "application_file",
        nargs="?",
        metavar="FILE",
        help="Path to a JSON credit-application file",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit a machine-readable JSON report (only the JSON is written to stdout)",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print the version and exit",
    )
    args = parser.parse_args(argv)

    if args.version:
        print(f"tvs-credit {__version__}")
        return 0

    if not args.application_file:
        parser.print_usage(sys.stderr)
        print("error: an application JSON FILE is required", file=sys.stderr)
        return 2

    # Load and validate input the same way the API does.
    try:
        raw = _load_application(args.application_file)
    except (OSError, ValueError) as e:
        print(f"error: could not read application file: {e}", file=sys.stderr)
        return 1

    errors = []
    try:
        application = CreditApplicationInput.model_validate(raw)
    except Exception as e:  # pydantic.ValidationError
        errors.append(f"invalid application data: {e}")
        application = None

    if application is not None:
        validation = validate_application_data(application)
        if not validation["valid"]:
            errors.extend(validation["errors"])

    if errors:
        for err in errors:
            print(f"error: {err}", file=sys.stderr)
        return 1

    assert application is not None
    scores = calculate_credit_score(application)
    explanation = generate_explanation(scores, application.model_dump())
    report = _build_report(scores, explanation)

    if args.json:
        try:
            json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
            sys.stdout.write("\n")
        except BrokenPipeError:
            # Downstream consumer (e.g. `... | head`) closed the pipe early.
            try:
                sys.stdout.close()
            except OSError:
                pass
            return 0
    else:
        print(_render_human(report))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)