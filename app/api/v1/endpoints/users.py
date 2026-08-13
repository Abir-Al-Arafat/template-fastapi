from typing import Any
from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_user
from app.schemas.user import User

router = APIRouter()


@router.get("/profile", response_model=User)
async def read_user_profile(
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get the profile details of the currently authenticated user."""
    return current_user
