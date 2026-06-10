from fastapi import FastAPI

from workflows.fraud_graph import (
    workflow
)

from models.claim_model import (
    Claim
)

app = FastAPI(
    title="Insurance Fraud AI Agent"
)


@app.get("/")
def health():

    return {
        "status":"running"
    }


@app.post("/analyze-claim")
def analyze_claim(
    claim: Claim
):

    result = workflow.invoke(

        {
            "claim":
                claim.model_dump()
        }
    )

    return {

        "claim_id":
            result["claim"]["claim_id"],

        "risk_score":
            result["risk_score"],

        "risk_level":
            result["risk_level"],

        "fraud_patterns":
            result["fraud_patterns"],

        "recommendation":
            result["recommendation"],

        "investigation_summary":
            result["investigation_summary"]
    }