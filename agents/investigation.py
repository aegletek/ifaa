import os
#from openai import OpenAI
from langfuse.openai import OpenAI
from dotenv import load_dotenv



from tools.langfuse_tool import (
    create_trace,
    log_event
)

load_dotenv()

client = OpenAI(
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
)


def build_prompt(state):

    return f"""
You are an insurance fraud analyst.

Analyze the claim and generate an investigation summary.

Claim Information:

{state["claim"]}

Historical Claims:

{state["history"].to_dict("records")}

Verification Result:

{state["verification"]}

Fraud Patterns:

{state["fraud_patterns"]}

Risk Score:

{state["risk_score"]}

Generate:

1. Fraud Assessment
2. Key Findings
3. Recommendation
"""


def run(state):

    trace = create_trace(
        "investigation_agent"
    )

    prompt = build_prompt(state)

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    summary = (
        response
        .choices[0]
        .message
        .content
    )

    state["investigation_summary"] = summary

    log_event(
        trace,
        "investigation_completed",
        {
            "claim_id": state["claim"]["claim_id"]
        }
    )

    return state