from tools.postgres_tool import (
    get_customer_claims
)

from tools.langfuse_tool import (
    create_trace,
    log_event
)


def run(state):

    trace = create_trace(
        "customer_history_agent"
    )

    customer_id = (
        state["claim"]
        ["customer_id"]
    )

    history = get_customer_claims(
        customer_id
    )

    log_event(

        trace,

        "history_retrieved",

        {
            "customer_id":
                customer_id,

            "records":
                len(history)
        }
    )

    state["history"] = history

    return state