from pydantic import BaseModel


class Claim(BaseModel):

    claim_id:str

    customer_id:str

    vehicle_number:str

    claim_amount:float

    claim_description:str