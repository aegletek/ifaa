import pandas as pd

from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:postgres@localhost:5432/frauddb"
)

customers = pd.read_csv(
    "mockdata/customers.csv"
)

claims = pd.read_csv(
    "mockdata/claims.csv"
)

customers.to_sql(
    "customers",
    engine,
    if_exists="append",
    index=False
)

claims.to_sql(
    "claims",
    engine,
    if_exists="append",
    index=False
)

print("Data Loaded")