from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from app.core.database import AsyncSession, get_db
from app.schemas.transaction import Transaction
from app.models.models import User, Account, Payment
from app.utils.signature import verify_signature
from app.core.config import settings

router = APIRouter(tags=["webhook"])


@router.post("/webhook")
async def webhook_handler(payload: Transaction, db: AsyncSession = Depends(get_db)):
    # Проверяем подпись
    data_dict = payload.model_dump()
    signature = payload.signature
    is_valid = verify_signature(
        data=data_dict, signature=signature, secret_key=settings.SECRET_KEY
    )

    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid signature")

    result = await db.execute(
        select(Payment).where(Payment.transaction_id == payload.transaction_id)
    )
    transaction = result.scalar_one_or_none()

    if transaction:
        return {"status": "already_processed"}

    result = await db.execute(select(Account).where(Account.id == payload.account_id))
    account_user = result.scalar_one_or_none()

    if not account_user:
        account_user = Account(
            id=payload.account_id, user_id=payload.user_id, balance=0
        )
        db.add(account_user)
        await db.flush()

    new_payment = Payment(
        transaction_id=payload.transaction_id,
        user_id=payload.user_id,
        account_id=payload.account_id,
        amount=payload.amount,
    )
    db.add(new_payment)

    account_user.balance += payload.amount
    db.add(account_user)

    await db.commit()

    return {"status": "ok"}
