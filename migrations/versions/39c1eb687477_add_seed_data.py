"""add seed data

Revision ID: 39c1eb687477
Revises: be62bb018794
Create Date: 2026-04-16 11:33:50.716983

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# revision identifiers, used by Alembic.
revision: str = '39c1eb687477'
down_revision: Union[str, None] = 'be62bb018794'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Вставляем пользователя и получаем его id
    result = op.execute(
        sa.text("""
            INSERT INTO users (email, hashed_password, full_name, role, created_at)
            VALUES ('user@example.com', :password, 'Test User', 'user', NOW())
            RETURNING id
        """),
        {"password": pwd_context.hash("user123")}
    )
    user_id = result.fetchone()[0]
    
    # Вставляем счёт с полученным user_id
    op.execute(
        sa.text("INSERT INTO accounts (user_id, balance) VALUES (:user_id, 1000)"),
        {"user_id": user_id}
    )
    
    op.execute(
        sa.text("""
            INSERT INTO users (email, hashed_password, full_name, role, created_at)
            VALUES ('admin@example.com', :password, 'Admin User', 'admin', NOW())
        """),
        {"password": pwd_context.hash("admin123")}
    )


def downgrade() -> None:
    pass
