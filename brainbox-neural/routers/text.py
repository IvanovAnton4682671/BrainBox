from core.logger import setup_logger
from fastapi import APIRouter, Request, Depends
from schemas.text import MessageText
from sqlalchemy.ext.asyncio import AsyncSession
from databases.postgresql import get_db
from interfaces.auth import auth_interface
from services.text import TextService
from repositories.text import TextRepository

logger = setup_logger("routers.text")

router = APIRouter(
    prefix="/text",
    tags=["Text"]
)

@router.post("/generate-answer")
async def generate_answer(request: Request, session: AsyncSession = Depends(get_db)):
    """
    Генерация и возврат ответа
    """
    try:
        logger.info("Получили запрос /generate-answer")
        session_id = request.headers.get("x-session-id")
        user_id = await auth_interface.get_user_id(session_id)
        request_data = await request.json()
        text = request_data.get("text")
        text_service = TextService(session)
        message_response = await text_service.create_answer(user_id, text)
        logger.info("Запрос выполнен, возвращаем результат")
        return {
            "success": True,
            "message_response": message_response
        }
    except Exception as e:
        logger.error(f"Ошибка генерации ответа: {str(e)}", exc_info=True)
        raise

@router.get("/get-text-messages")
async def get_text_messages(request: Request, session: AsyncSession = Depends(get_db)):
    """
    Загрузка всей истории чата пользователя
    """
    try:
        logger.info("Получили запрос /get-text-messages")
        session_id = request.headers.get("x-session-id")
        user_id = await auth_interface.get_user_id(session_id)
        text_service = TextService(session)
        messages = await text_service.get_messages(user_id)
        if messages is None:
            logger.info("messages is None, возвращаем пустой массив")
            return {"success": True, "messages": []}
        logger.info("Запрос выполнен, возвращаем результат")
        return {
            "success": True,
            "messages": messages
        }
    except Exception as e:
        logger.error(f"Ошибка загрузки истории чата пользователя: {str(e)}", exc_info=True)
        raise

@router.delete("/delete-text-messages")
async def delete_text_messages(request: Request, session: AsyncSession = Depends(get_db)):
    """
    Удаляет всю историю чата пользователя
    """
    try:
        logger.info("Получили запрос /delete-text-messages")
        session_id = request.headers.get("x-session-id")
        user_id = await auth_interface.get_user_id(session_id)
        text_service = TextService(session)
        await text_service.delete_messages(user_id)
        logger.info("Запрос выполнен, возвращаем результат")
        return {
            "success": True
        }
    except Exception as e:
        logger.error(f"Ошибка удаления истории чата пользователя: {str(e)}", exc_info=True)
        raise