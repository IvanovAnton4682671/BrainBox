from core.logger import setup_logger
from core.config import settings
import httpx

logger = setup_logger("interfaces.auth")

class AuthInterface:
    def __init__(self):
        self.base_url = f"{settings.AUTH_SERVICE_URL}/auth"
        self.client = httpx.AsyncClient()

    async def get_user_id(self, session_id: str) -> int:
        try:
            logger.info(f"Отправили запрос на /check-session с session_id={session_id}")
            response = await self.client.get(
                f"{self.base_url}/check-session",
                cookies={"sessionid": session_id},
                timeout=5.0
            )
            response.raise_for_status()
            logger.info(f"Детальный результат: {response.json()}")
            return response.json()["user_id"]
        except Exception as e:
            logger.error(f"Ошибка при выполнении запроса: {str(e)}", exc_info=True)
            raise

auth_interface = AuthInterface()