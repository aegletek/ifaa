import os

import pandas as pd

from sqlalchemy import create_engine

from dotenv import load_dotenv

load_dotenv()

connection_string = (

    f"postgresql://"
    f"{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"

)

engine = create_engine(
    connection_string
)


def get_customer_claims(customer_id):

    query = f"""

    SELECT *

    FROM claims

    WHERE customer_id='{customer_id}'

    """

    return pd.read_sql(
        query,
        engine
    )