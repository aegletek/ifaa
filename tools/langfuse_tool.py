import os

from dotenv import load_dotenv

from langfuse import Langfuse

load_dotenv()

langfuse = Langfuse(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

'''
def create_trace(trace_name):

    trace = langfuse.trace(
        name=trace_name
    )

    return trace


def log_event(trace, event_name, metadata):

    trace.event(
        name=event_name,
        metadata=metadata
    )
'''

def create_trace(trace_name):
    return None

def log_event(trace, event_name, metadata):
    pass