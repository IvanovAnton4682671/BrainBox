from fastapi import APIRouter, Depends
from core.errors import error_handler
from schemas.user import UserCreate, UserAuth
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from services.user import UserService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=dict)
@error_handler
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Регистрация нового пользователя
    """
    service = UserService(db)
    user = await service.register_user(user_data)
    return {
        "success": True,
        "message": "Пользователь успешно зарегистрирован!",
        "user_id": user.id
    }

@router.post("/login", response_model=dict)
@error_handler
async def login_user(user_data: UserAuth, db: AsyncSession = Depends(get_db)):
    """
    Авторизация пользователя
    """
    service = UserService(db)
    user = await service.auth_user(user_data)
    return {
        "success": True,
        "message": "Пользователь успешно авторизован!",
        "user_id": user.id
    }