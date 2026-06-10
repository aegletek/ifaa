
import os

from dotenv import load_dotenv
from langfuse import Langfuse

load_dotenv()

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)


def create_trace(claim_id):

    trace = langfuse.create_trace(
        name="insurance_fraud_detection",
        user_id=claim_id
    )

    return trace


def log_event(trace, name, metadata=None):

    span = trace.span(
        name=name
    )

    if metadata:
        span.update(
            metadata=metadata
        )

    return span