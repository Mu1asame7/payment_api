from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from app.core.database import AsyncSession, get_db
from sqlalchemy import select
from app.schemas.account import AccountOut
from app.models.models import User, Account
from app.core.dependencies import get_current_user


router = APIRouter(tags=["accounts"])


@router.get("/accounts", response_model=list[AccountOut])
async def get_accounts(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Account).where(Account.user_id == current_user.id))
    accounts = result.scalars().all()

    if not accounts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no accounts that meet the conditions",
        )

    return accounts
