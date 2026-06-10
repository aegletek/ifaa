from datetime import datetime

from uuid import uuid4

from tools.langfuse_tool import (
    create_trace,
    log_event
)


REQUIRED_FIELDS = [

    "claim_id",

    "customer_id",

    "vehicle_number",

    "claim_amount",

    "claim_description"
]


def validate_claim(claim):

    missing_fields = []

    for field in REQUIRED_FIELDS:

        if field not in claim:

            missing_fields.append(
                field
            )

    if missing_fields:

        raise Exception(
            f"Missing Fields : "
            f"{missing_fields}"
        )


def normalize_claim(claim):

    claim["vehicle_number"] = (

        claim["vehicle_number"]

        .replace(" ", "")

        .upper()

    )

    claim["claim_description"] = (

        claim["claim_description"]

        .strip()

    )

    claim["claim_amount"] = float(
        claim["claim_amount"]
    )

    return claim


def enrich_claim(claim):

    claim["received_at"] = str(
        datetime.utcnow()
    )

    claim["workflow_id"] = str(
        uuid4()
    )

    claim["status"] = "RECEIVED"

    return claim


def run(state):

    trace = create_trace(
        "claim_intake"
    )

    claim = state["claim"]

    validate_claim(claim)

    claim = normalize_claim(
        claim
    )

    claim = enrich_claim(
        claim
    )

    log_event(

        trace,

        "claim_received",

        {

            "claim_id":
                claim["claim_id"],

            "customer_id":
                claim["customer_id"]

        }
    )

    state["claim"] = claim

    return state