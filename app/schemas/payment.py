from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime


class PaymentOut(BaseModel):
    id: int
    transaction_id: str
    account_id: int
    amount: Decimal
    created_at: datetime
