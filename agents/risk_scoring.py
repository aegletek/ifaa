from tools.fraud_rules import evaluate_claim

from tools.langfuse_tool import (
    create_trace,
    log_event
)


def determine_risk_level(score):

    if score >= 80:
        return "HIGH"

    if score >= 50:
        return "MEDIUM"

    return "LOW"


def recommendation(level):

    mapping = {

        "HIGH":
            "Manual Investigation Required",

        "MEDIUM":
            "Review By Claims Team",

        "LOW":
            "Approve Claim"
    }

    return mapping[level]


def run(state):

    trace = create_trace(
        "risk_scoring_agent"
    )

    claim = state["claim"]

    history = state["history"]

    result = evaluate_claim(
        claim,
        history
    )

    risk_score = result["risk_score"]

    risk_level = determine_risk_level(
        risk_score
    )

    state["risk_score"] = risk_score

    state["risk_level"] = risk_level

    state["fraud_patterns"] = (
        result["fraud_patterns"]
    )

    state["recommendation"] = (
        recommendation(
            risk_level
        )
    )

    log_event(

        trace,

        "risk_calculated",

        {

            "risk_score":
                risk_score,

            "risk_level":
                risk_level,

            "patterns":
                result["fraud_patterns"]

        }
    )

    return state