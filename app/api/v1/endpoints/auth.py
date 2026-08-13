from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import create_access_token
from app.schemas.user import User as UserSchema, UserCreate
from app.services.user_service import user_service

router = APIRouter()


@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def register(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Create user with hashed password (accepts JSON or Form fields: name, email, password)."""
    content_type = request.headers.get("content-type", "")
    
    email: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None
    
    if "application/json" in content_type:
        try:
            body = await request.json()
            email = body.get("email")
            password = body.get("password")
            name = body.get("name")
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON body"
            )
    elif "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
        form_data = await request.form()
        email = form_data.get("email")
        password = form_data.get("password")
        name = form_data.get("name")
    else:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported media type. Must be application/json or form-data"
        )
        
    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required"
        )
        
    try:
        user_in = UserCreate(email=email, password=password, name=name)
        user = await user_service.create_user(db, user_in)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login")
async def login(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Authenticate user via email & password, return JWT bearer access token."""
    content_type = request.headers.get("content-type", "")
    
    email: Optional[str] = None
    password: Optional[str] = None
    
    if "application/json" in content_type:
        try:
            body = await request.json()
            email = body.get("email")
            password = body.get("password")
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON body"
            )
    elif "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
        form_data = await request.form()
        # OAuth2 password request form fields are 'username' and 'password'
        email = form_data.get("username") or form_data.get("email")
        password = form_data.get("password")
    else:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported media type. Must be application/json or form-data"
        )
        
    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email/Username and password are required"
        )
        
    user = await user_service.authenticate(db, email=email, password=password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
        
    access_token = create_access_token(subject=user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
