from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from app.core.database import AsyncSession, get_db
from app.core.dependencies import get_current_admin
from app.core.security import get_password_hash
from app.models.models import User, Account
from app.schemas.user import UserOut, UserCreate
from app.schemas.account import AccountOut


router = APIRouter(tags=["admin"])


@router.get("/admin/users", response_model=list[UserOut])
async def get_all_users(
    admin: User = Depends(get_current_admin), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


@router.post("/admin/users", response_model=UserOut)
async def create_user(
    user_data: UserCreate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.email == user_data.email))
    user = result.scalar_one_or_none()

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    hashed_password = get_password_hash(user_data.password)

    user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        role=user_data.role,
    )

    db.add(user)
    await db.commit()

    return user


@router.put("/admin/users/{user_id}", response_model=UserOut)
async def update_user(
    user_id: int,
    user_data: UserCreate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Проверка уникальности email
    result = await db.execute(
        select(User).where(User.email == user_data.email, User.id != user_id)
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already in use")

    user.email = user_data.email
    user.full_name = user_data.full_name
    user.role = user_data.role
    user.hashed_password = get_password_hash(user_data.password)

    await db.commit()
    await db.refresh(user)

    return user


@router.delete("/admin/users/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()


@router.get("/admin/users/{user_id}/accounts", response_model=list[AccountOut])
async def get_user_account(
    user_id: int,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Account).where(Account.user_id == user_id))
    accounts = result.scalars().all()
    return accounts
