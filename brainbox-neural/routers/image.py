from core.logger import setup_logger
from fastapi import APIRouter, Request, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from databases.postgresql import get_db
from interfaces.auth import auth_interface
from services.image import ImageService
from schemas.image import ImageMessageRequest
from core.storage import image_storage

logger = setup_logger("routers.image")

router = APIRouter(
    prefix="/image",
    tags=["Image"]
)

@router.post("/generate-answer")
async def generate_answer(request: Request, session: AsyncSession = Depends(get_db)):
    """
    Генерация и возврат image_uid для последующего взаимодействия
    """
    try:
        logger.info("Получили запрос /generate-answer")
        session_id = request.headers.get("x-session-id")
        user_id = await auth_interface.get_user_id(session_id)
        image_service = ImageService(session)
        request_data = await request.json()
        text = request_data.get("text")
        user_message = ImageMessageRequest(
            user_id=user_id,
            message_text=text
        )
        response = await image_service.create_answer(user_message)
        logger.info("Запрос выполнили, возвращаем результат")
        return {
            "success": True,
            "image_uid": str(response.image_uid)
        }
    except Exception as e:
        logger.error(f"Ошибка создания картинки: {str(e)}", exc_info=True)
        raise

@router.get("/view/{image_uid}")
async def view_image(request: Request, image_uid: str, session: AsyncSession = Depends(get_db)):
    """
    Отображение картинки по image_uid
    """
    try:
        logger.info("Пришёл запрос /view/{image_uid}")
        image = await image_storage.download_image(image_uid)
        logger.info("Запрос выполнили, возвращаем результат")
        return Response(
            content=image,
            media_type="image/jpeg",
            headers={"Cache-Control": "public, max-age=3600"}
        )
    except Exception as e:
        logger.error(f"Ошибка отображения картинки: {str(e)}", exc_info=True)
        raise

@router.get("/download/{image_uid}")
async def download_image(request: Request, image_uid: str, session: AsyncSession = Depends(get_db)):
    try:
        logger.info("Получили запрос /download/{image_uid}")
        image = await image_storage.download_image(image_uid)
        image_name = f"image_{image_uid}.jpg"
        logger.info("Запрос выполнили, возвращаем результат")
        return Response(
            content=image,
            media_type="image/jpeg",
            headers={
                "Content-Disposition": f"attachment; filename={image_name}",
                "Cache-Control": "public, max-age=3600"
            }
        )
    except Exception as e:
        logger.error(f"Ошибка при скачивании картинки: {str(e)}", exc_info=True)
        raise

@router.get("/get-image-messages")
async def get_image_messages(request: Request, session: AsyncSession = Depends(get_db)):
    """
    Получение истории чата
    """
    try:
        logger.info("Получили запрос /get-image-messages")
        session_id = request.headers.get("x-session-id")
        user_id = await auth_interface.get_user_id(session_id)
        image_service = ImageService(session)
        messages = await image_service.get_user_messages(user_id)
        if messages is None:
            logger.info("messages is None, возвращаем пустой массив")
            return {"success": True, "messages": []}
        logger.info("Запрос выполнен, возвращаем сообщения")
        return {
            "success": True,
            "messages": messages
        }
    except Exception as e:
        logger.error(f"Ошибка получения истории чата: {str(e)}", exc_info=True)
        raise

@router.delete("/delete-image-messages")
async def delete_image_messages(request: Request, session: AsyncSession = Depends(get_db)):
    try:
        logger.info("Получили запрос /delete-image-messages")
        session_id = request.headers.get("x-session-id")
        user_id = await auth_interface.get_user_id(session_id)
        image_service = ImageService(session)
        await image_service.delete_user_messages(user_id)
        logger.info("Запрос выполнили, возвращаем результат")
        return {"success": True}
    except Exception as e:
        logger.error(f"Ошибка удаления сообщений: {str(e)}", exc_info=True)
        raise