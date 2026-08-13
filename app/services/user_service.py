from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.repositories.user_repository import user_repository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """Business logic for users."""

    def __init__(self):
        self.repository = user_repository

    async def create_user(
        self,
        db: AsyncSession,
        user_in: UserCreate
    ) -> User:
        """Create a new user with a hashed password."""
        existing = await self.repository.get_by_email(db, user_in.email)
        if existing:
            raise ValueError("Email already registered")

        user_in_dict = user_in.model_dump()
        password = user_in_dict.pop("password")
        user_in_dict["hashed_password"] = get_password_hash(password)

        # Create user using repository
        db_obj = self.repository.model(**user_in_dict)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def authenticate(
        self,
        db: AsyncSession,
        email: str,
        password: str
    ) -> Optional[User]:
        """Authenticate user by email and password."""
        user = await self.repository.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def update_user(
        self,
        db: AsyncSession,
        user_id: int,
        user_in: UserUpdate
    ) -> Optional[User]:
        """Update a user's details, hashing the password if provided."""
        user = await self.repository.get(db, user_id)
        if not user:
            return None

        user_in_dict = user_in.model_dump(exclude_unset=True)
        if "password" in user_in_dict:
            password = user_in_dict.pop("password")
            user_in_dict["hashed_password"] = get_password_hash(password)

        return await self.repository.update(db, db_obj=user, obj_in=user_in_dict)


user_service = UserService()
