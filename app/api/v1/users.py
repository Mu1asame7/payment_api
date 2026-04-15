from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.schemas.user import UserOut
from app.models.models import User

router = APIRouter(tags=["users"])


@router.get("/users/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
