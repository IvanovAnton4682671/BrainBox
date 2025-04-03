from fastapi import APIRouter, Depends, HTTPException
from schemas.user import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from services.user_service import UserService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register")
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Регистрация нового пользователя
    """
    service = UserService(db)
    user = await service.register_user(user_data)
    if not user:
        raise HTTPException(status_code=400, detail="Email or name already exists!")
    return {"message": "User created successfully!", "user_id": user.id}

@router.post("/login")
async def login_user(
    user_email: str,
    user_password: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Авторизация пользователя
    """
    service = UserService(db)
    user = await service.auth_user(user_email, user_password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials!")
    return {"message": "Login successfully!", "user_id": user.id}