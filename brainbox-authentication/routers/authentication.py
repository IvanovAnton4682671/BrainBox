from core.logger import setup_logger
from fastapi import APIRouter, Depends, Response, Request
from core.errors import error_handler
from schemas.user import UserCreate, UserAuth
from sqlalchemy.ext.asyncio import AsyncSession
from databases.postgresql import get_db
from services.user import UserService

logger = setup_logger("routers.authentication")

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=dict)
@error_handler
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db), response: Response = None):
    """
    Регистрация нового пользователя
    """
    logger.info("Получили запрос /register")
    service = UserService(db)
    register_data = await service.register_user(user_data)
    logger.info(f"Получили register_data = {register_data}")
    response.set_cookie(
        key="sessionid",
        value=register_data["sessionid"],
        httponly=True,
        secure=False, #не только HTTPS
        samesite="lax",
        max_age=86400,
        path="/",
        domain=None
    )
    logger.info(f"Отправили в ответе user_id = {register_data["user"].id}")
    return {
        "success": True,
        "message": "Пользователь успешно зарегистрирован!",
        "user_id": register_data["user"].id
    }

@router.post("/login", response_model=dict)
@error_handler
async def login_user(user_data: UserAuth, db: AsyncSession = Depends(get_db), response: Response = None):
    """
    Авторизация пользователя
    """
    logger.info(f"Получили запрос /login")
    service = UserService(db)
    login_data = await service.auth_user(user_data)
    logger.info(f"Получили login_data = {login_data}")
    response.set_cookie(
        key="sessionid",
        value=login_data["sessionid"],
        httponly=True,
        secure=False, #не только HTTPS
        samesite="lax",
        max_age=86400,
        path="/",
        domain=None
    )
    logger.info(f"Отправили в ответе user_id = {login_data["user"].id}")
    return {
        "success": True,
        "message": "Пользователь успешно авторизован!",
        "user_id": login_data["user"].id
    }

@router.get("/check-session", response_model=dict)
@error_handler
async def check_user_session(request: Request, db: AsyncSession = Depends(get_db)):
    """
    Проверка валидности сессии
    """
    logger.info(f"Получили запрос /check-session")
    service = UserService(db)
    user = await service.get_user_profile(request.state.user_id)
    logger.info(f"Получили user = {user}")
    logger.info(f"Отправили в ответе user_id = {user.id}, user_name = {user.name}")
    return {
        "success": True,
        "message": "Сессия пользователя существует!",
        "user_id": user.id,
        "user_name": user.name
    }

@router.post("/logout", response_model=dict)
@error_handler
async def logout_user(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    """
    Удаление сессии пользователя
    """
    logger.info(f"Получили запрос /logout")
    sessionid = request.cookies.get("sessionid")
    if sessionid:
        try:
            logger.info(f"Получили sessionid = {sessionid}")
            service = UserService(db)
            await service.logout_user(sessionid)
            response.delete_cookie("sessionid", path="/", domain=None)
            logger.info(f"Удалили sessionid")
            logger.info("Отправили в ответе success = True")
            return {
                "success": True,
                "message": "Сессия пользователя завершена!"
            }
        except Exception as e:
            logger.error(f"Ошибка при удалении сессии: {str(e)}", exc_info=True)
            raise
    logger.warning("Не получили sessionid")
    logger.warning("Отправили в ответе success = False")
    return {
        "success": False,
        "message": "Сессия не найдена!"
    }