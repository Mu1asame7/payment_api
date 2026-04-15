from passlib.context import CryptContext
from jose import jwt
from app.core.config import settings
from datetime import datetime, timezone, timedelta

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Хешируем пароль"""
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Проверка совпадения пароля с хешем"""
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict) -> str:
    """Создаем JWT токен"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    return payload
