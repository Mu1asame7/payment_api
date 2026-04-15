from pydantic import BaseModel
from decimal import Decimal


class AccountOut(BaseModel):
    id: int
    balance: Decimal
    user_id: int
