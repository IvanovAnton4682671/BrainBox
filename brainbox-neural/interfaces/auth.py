from core.logger import setup_logger
from core.config import settings
import httpx

logger = setup_logger("interfaces/auth.py")

class AuthService:
    def __init__(self):
        self.base_url = f"{settings.AUTH_SERVICE_URL}/auth"
        self.client = httpx.AsyncClient()

    async def get_user_id(self, session_id: str) -> int:
        try:
            response = await self.client.get(
                f"{self.base_url}/check-session",
                cookies={"sessionid": session_id},
                timeout=5.0
            )
            response.raise_for_status()
            return response.json()["user_id"]
        except Exception as e:
            raise

auth_service = AuthService()