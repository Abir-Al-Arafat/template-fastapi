from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    """Shared properties for user schemas."""
    email: EmailStr
    name: Optional[str] = None
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    """Properties required to create a user."""
    password: str


class UserUpdate(BaseModel):
    """Properties to receive on user update."""
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class User(UserBase):
    """Properties returned to the client (User Response schema)."""
    model_config = ConfigDict(from_attributes=True)

    id: int
