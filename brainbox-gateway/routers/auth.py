from core.logger import setup_logger
from fastapi import APIRouter, Request, Response, status
from fastapi.exceptions import HTTPException
from interfaces.auth import auth_interface
import httpx

logger = setup_logger("routers.auth")

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

async def _process_auth_response(auth_response: httpx.Response, response: Response):
    #устанавливаем куки, если они есть
    if "set-cookie" in auth_response.headers:
        response.headers["set-cookie"] = auth_response.headers["set-cookie"]
        logger.info("Установили куки в заголовки ответа")
    response_data = auth_response.json() #получаем данные как есть
    logger.info(f"Получили response_data = {response_data}")
    #если есть ошибка - возвращаем её как есть
    if auth_response.is_error:
        detail = response_data.get("detail")
        logger.warning(f"Получили ошибку: detail = {detail}, status_code = {auth_response.status_code}")
        raise HTTPException(
            status_code=auth_response.status_code,
            detail={
                "success": detail.get("success"),
                "error": detail.get("error")
            }
        )
    logger.info(f"Отправили в ответе response_data = {response_data}")
    return response_data

@router.post("/register")
async def register_user(request: Request, response: Response):
    logger.info("Получили запрос /register")
    user_data = await request.json()
    logger.info(f"Получили user_data = {user_data}")
    auth_response = await auth_interface.register(user_data)
    logger.info(f"Получили auth_response = {auth_response}")
    return await _process_auth_response(auth_response, response)

@router.post("/login")
async def login_user(request: Request, response: Response):
    logger.info("Получили запрос /login")
    user_data = await request.json()
    logger.info(f"Получили user_data = {user_data}")
    auth_response = await auth_interface.login(user_data)
    logger.info(f"Получили auth_response = {auth_response}")
    return await _process_auth_response(auth_response, response)

@router.get("/check-session")
async def check_session(request: Request, response: Response):
    logger.info("Получили запрос /check-session")
    cookies = request.cookies
    logger.info(f"Получили cookies = {cookies}")
    auth_response = await auth_interface.check_session(cookies)
    logger.info(f"Получили auth_response = {auth_response}")
    return await _process_auth_response(auth_response, response)

@router.post("/logout")
async def logout(request: Request, response: Response):
    logger.info("Получили запрос /logout")
    cookies = request.cookies
    logger.info(f"Получили cookies = {cookies}")
    auth_response = await auth_interface.logout(cookies)
    logger.info(f"Получили auth_response = {auth_response}")
    return await _process_auth_response(auth_response, response)