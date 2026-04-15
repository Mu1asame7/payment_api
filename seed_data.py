import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.models import User, Account, Payment
from app.core.security import get_password_hash

normal_user = {
    "email": "user@example.com",
    "password": "user123",
    "full_name": "Test User",
    "role": "user",
}
admin = {
    "email": "admin@example.com",
    "password": "admin123",
    "full_name": "Admin User",
    "role": "admin",
}


async def seed():
    async with AsyncSessionLocal() as session:
        # Создание тестового пользователя
        result = await session.execute(
            select(User).where(User.email == normal_user["email"])
        )
        existing_user = result.scalar_one_or_none()

        if not existing_user:
            user = User(
                email=normal_user["email"],
                hashed_password=get_password_hash(normal_user["password"]),
                full_name=normal_user["full_name"],
                role=normal_user["role"],
            )
            session.add(user)
            await session.flush()
            user_id = user.id
        else:
            user_id = existing_user.id

        # Создание администратора
        result = await session.execute(select(User).where(User.email == admin["email"]))
        existing_admin = result.scalar_one_or_none()

        if not existing_admin:
            administrator = User(
                email=admin["email"],
                hashed_password=get_password_hash(admin["password"]),
                full_name=admin["full_name"],
                role=admin["role"],
            )
            session.add(administrator)

        # Создание счета
        result = await session.execute(
            select(Account).where(Account.user_id == user_id)
        )
        existing_account = result.scalar_one_or_none()
        if not existing_account:
            account_user = Account(user_id=user_id, balance=1000)
            session.add(account_user)

        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
