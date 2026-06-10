from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    END
)

from agents.claim_intake import run as intake

from agents.customer_history import (
    run as history
)

from agents.external_verification import (
    run as verification
)

from agents.risk_scoring import (
    run as risk
)

from agents.investigation import (
    run as investigation
)


class FraudState(TypedDict):

    claim:dict

    history:object

    verification:dict

    risk_score:int

    risk_level:str

    fraud_patterns:list

    recommendation:str

    investigation_summary:str


builder = StateGraph(
    FraudState
)

builder.add_node(
    "intake",
    intake
)

builder.add_node(
    "history",
    history
)

builder.add_node(
    "verification",
    verification
)

builder.add_node(
    "risk",
    risk
)

builder.add_node(
    "investigation",
    investigation
)

builder.set_entry_point(
    "intake"
)

builder.add_edge(
    "intake",
    "history"
)

builder.add_edge(
    "history",
    "verification"
)

builder.add_edge(
    "verification",
    "risk"
)

builder.add_edge(
    "risk",
    "investigation"
)

builder.add_edge(
    "investigation",
    END
)

workflow = builder.compile()