from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from app.core.database import AsyncSession, get_db
from sqlalchemy import select
from app.schemas.payment import PaymentOut
from app.models.models import User, Payment
from app.core.dependencies import get_current_user


router = APIRouter(tags=["payments"])


@router.get("/payments", response_model=list[PaymentOut])
async def get_payments(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Payment).where(Payment.user_id == current_user.id))
    payments = result.scalars().all()

    if not payments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no payments that meet the conditions",
        )

    return payments
