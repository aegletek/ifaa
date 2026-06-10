import random

from tools.langfuse_tool import (
    create_trace,
    log_event
)


def vehicle_verification(vehicle):

    return {

        "vehicle_found": True,

        "registration_valid": True
    }


def accident_verification(vehicle):

    probability = random.random()

    if probability > 0.2:

        return {

            "accident_record_found": True
        }

    return {

        "accident_record_found": False
    }


def run(state):

    trace = create_trace(
        "external_verification_agent"
    )

    vehicle_number = (

        state["claim"]
        ["vehicle_number"]
    )

    vehicle_result = (

        vehicle_verification(
            vehicle_number
        )
    )

    accident_result = (

        accident_verification(
            vehicle_number
        )
    )

    verification = {

        **vehicle_result,

        **accident_result
    }

    log_event(

        trace,

        "verification_complete",

        verification
    )

    state["verification"] = verification

    return state