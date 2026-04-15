from pydantic import BaseModel
from decimal import Decimal


class Transaction(BaseModel):
    transaction_id: str
    user_id: int
    account_id: int
    amount: Decimal
    signature: str