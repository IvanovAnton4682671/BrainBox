from fastapi import APIRouter, Request, Response, status
from fastapi.exceptions import HTTPException
from interfaces.auth import auth_service
import httpx
from core.logger import setup_logger

logger = setup_logger("routers/auth.py")

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

async def _process_auth_response(auth_response: httpx.Response, response: Response):
    #устанавливаем куки, если они есть
    if "set-cookie" in auth_response.headers:
        response.headers["set-cookie"] = auth_response.headers["set-cookie"]
    response_data = auth_response.json() #получаем данные как есть
    #если есть ошибка - возвращаем её как есть
    if auth_response.is_error:
        detail = response_data.get("detail")
        raise HTTPException(
            status_code=auth_response.status_code,
            detail={
                "success": detail.get("success"),
                "error": detail.get("error")
            }
        )
    return response_data

@router.post("/register")
async def register_user(request: Request, response: Response):
    user_data = await request.json()
    auth_response = await auth_service.register(user_data)
    return await _process_auth_response(auth_response, response)

@router.post("/login")
async def login_user(request: Request, response: Response):
    user_data = await request.json()
    auth_response = await auth_service.login(user_data)
    return await _process_auth_response(auth_response, response)

@router.get("/check-session")
async def check_session(request: Request, response: Response):
    cookies = request.cookies
    auth_response = await auth_service.check_session(cookies)
    return await _process_auth_response(auth_response, response)

@router.post("/logout")
async def logout(request: Request, response: Response):
    cookies = request.cookies
    auth_response = await auth_service.logout(cookies)
    return await _process_auth_response(auth_response, response)