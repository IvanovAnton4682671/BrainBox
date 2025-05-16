from core.config import settings
from core.logger import setup_logger
import httpx

logger = setup_logger("interfaces/auth.py")

class AuthInterface:
    def __init__(self):
        self.base_url = f"{settings.AUTH_SERVICE_URL}/auth"
        self.client = httpx.AsyncClient(timeout=30.0)

    async def register(self, user_data: dict):
        logger.info("Получен /register запрос для сервиса аутентификации!")
        return await self.client.post(
            f"{self.base_url}/register",
            json=user_data
        )

    async def login(self, user_data: dict):
        logger.info("Получен /login запрос для сервиса аутентификации!")
        return await self.client.post(
            f"{self.base_url}/login",
            json=user_data
        )

    async def check_session(self, cookies: dict):
        logger.info("Получен /check-session запрос для сервиса аутентификации!")
        return await self.client.get(
            f"{self.base_url}/check-session",
            cookies=cookies
        )

    async def logout(self, cookies: dict):
        logger.info("Получен /logout запрос для сервиса аутентификации!")
        return await self.client.post(
            f"{self.base_url}/logout",
            cookies=cookies
        )

auth_interface = AuthInterface()