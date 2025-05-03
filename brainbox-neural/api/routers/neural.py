from core.logger import setup_logger
from fastapi import APIRouter, Request, UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from databases.postgres import get_db
from services.audio import AudioService
from interfaces.auth import auth_service
from repositories.audio import AudioRepository
from core.storage import audio_storage
from schemas.audio import AudioMessageCreate
from fastapi import Response

logger = setup_logger("api/routers/neural.py")

router = APIRouter(
    prefix="/neural",
    tags=["Neural"]
)

@router.post("/upload-audio")
async def upload_audio(request: Request, file: UploadFile, db: AsyncSession = Depends(get_db)):
    """
    Сохраняет файл в MinIO
    """
    try:
        session_id = request.headers.get("x-session-id")
        user_id = await auth_service.get_user_id(session_id)
        file_data = await file.read()
        audio_uid = await audio_storage.upload_audio(file_data)
        audio_repo = AudioRepository(db)
        await audio_repo.create_message(AudioMessageCreate(
            user_id=user_id,
            is_from_user=True,
            message_text=file.filename,
            audio_uid=audio_uid
        ))
        return {
            "success": True,
            "filename": file.filename,
            "audio_uid": audio_uid
        }
    except Exception as e:
        raise

@router.post("/recognize-saved-audio")
async def recognize_saved_audio(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        session_id = request.headers.get("x-session-id")
        user_id = await auth_service.get_user_id(session_id)
        audio_service = AudioService(db)
        request_data = await request.json()
        audio_uid = request_data.get("audio_uid")
        return await audio_service.recognize_saved_audio(user_id=user_id, audio_uid=audio_uid)
    except Exception as e:
        raise

@router.get("/get-audio-messages")
async def get_audio_messages(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        session_id = request.headers.get("x-session-id")
        user_id = await auth_service.get_user_id(session_id)
        audio_repo = AudioRepository(db)
        messages = await audio_repo.get_user_messages(user_id)
        return { "success": True, "messages": messages }
    except Exception as e:
        raise

@router.get("/download-audio/{audio_uid}")
async def download_audio(audio_uid: str, request: Request, db: AsyncSession = Depends(get_db)):
    try:
        session_id = request.headers.get("x-session-id")
        user_id = await auth_service.get_user_id(session_id)
        audio_repo = AudioRepository(db)
        message = await audio_repo.get_message_by_uid(audio_uid)
        if not message or message.user_id != user_id:
            raise ValueError("Audio not found")
        audio_data = await audio_storage.download_audio(audio_uid)
        return Response(
            content=audio_data,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f"attachment; filename={message.message_text}"
            }
        )
    except Exception as e:
        raise