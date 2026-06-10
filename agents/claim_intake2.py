from datetime import datetime
from uuid import uuid4

from langfuse import Langfuse
import os

langfuse = Langfuse(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host=os.getenv("LANGFUSE_HOST")
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
            missing_fields.append(field)

    if missing_fields:

        raise Exception(
            f"Missing fields : {missing_fields}"
        )

    if float(claim["claim_amount"]) <= 0:

        raise Exception(
            "Invalid claim amount"
        )

    return True


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

    claim["received_timestamp"] = str(
        datetime.utcnow()
    )

    claim["workflow_id"] = str(
        uuid4()
    )

    claim["status"] = "RECEIVED"

    return claim


def run(state):

    claim = state["claim"]

    trace = langfuse.trace(
        name="claim_intake_agent"
    )

    validate_claim(claim)

    claim = normalize_claim(claim)

    claim = enrich_claim(claim)

    trace.event(
        name="claim_received",
        metadata={
            "claim_id": claim["claim_id"],
            "customer_id": claim["customer_id"]
        }
    )

    state["claim"] = claim

    state["claim_intake_completed"] = True

    return state