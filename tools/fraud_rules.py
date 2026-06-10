import os
from dotenv import load_dotenv
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)


# ----------------------------------------
# Embedding Utility
# ----------------------------------------

def get_embedding(text):

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


def similarity_score(text1, text2):

    emb1 = get_embedding(text1)

    emb2 = get_embedding(text2)

    score = cosine_similarity(
        [emb1],
        [emb2]
    )[0][0]

    return float(score)


# ----------------------------------------
# Rule 1
# Duplicate Claim
# ----------------------------------------

def duplicate_claim_rule(claim, history):

    matches = history[
        (
            history["vehicle_number"]
            ==
            claim["vehicle_number"]
        )
    ]

    if len(matches) > 0:

        return {
            "fraud": True,
            "score": 40,
            "reason": "Duplicate Claim Fraud"
        }

    return {
        "fraud": False,
        "score": 0,
        "reason": None
    }


# ----------------------------------------
# Rule 2
# Inflated Amount
# ----------------------------------------

def inflated_amount_rule(claim, history):

    if len(history) == 0:

        return {
            "fraud": False,
            "score": 0,
            "reason": None
        }

    avg_amount = history.claim_amount.mean()

    if claim["claim_amount"] > avg_amount * 2:

        return {
            "fraud": True,
            "score": 30,
            "reason": (
                f"Inflated Claim Amount "
                f"(Historical Avg={avg_amount})"
            )
        }

    return {
        "fraud": False,
        "score": 0,
        "reason": None
    }


# ----------------------------------------
# Rule 3
# Similar Claim Fraud
# ----------------------------------------

def repeated_similar_claim_rule(
    claim,
    history
):

    for _, row in history.iterrows():

        score = similarity_score(
            claim["claim_description"],
            row["claim_description"]
        )

        if score > 0.90:

            return {
                "fraud": True,
                "score": 30,
                "reason":
                    f"Repeated Similar Claim "
                    f"Similarity={round(score,2)}"
            }

    return {
        "fraud": False,
        "score": 0,
        "reason": None
    }


# ----------------------------------------
# Rule Executor
# ----------------------------------------

def evaluate_claim(claim, history):

    results = []

    results.append(
        duplicate_claim_rule(
            claim,
            history
        )
    )

    results.append(
        inflated_amount_rule(
            claim,
            history
        )
    )

    results.append(
        repeated_similar_claim_rule(
            claim,
            history
        )
    )

    score = 0

    fraud_patterns = []

    for result in results:

        score += result["score"]

        if result["fraud"]:

            fraud_patterns.append(
                result["reason"]
            )

    return {

        "risk_score":
            min(score, 100),

        "fraud_patterns":
            fraud_patterns
    }