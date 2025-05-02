from core.logger import setup_logger
from fastapi import APIRouter, Request, UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from databases.postgres import get_db
from services.audio import AudioService
from interfaces.auth import auth_service
from repositories.audio import AudioRepository

logger = setup_logger("api/routers/neural.py")

router = APIRouter(
    prefix="/neural",
    tags=["Neural"]
)

@router.post("/recognize-audio")
async def recognize_audio(request: Request, file: UploadFile, db: AsyncSession = Depends(get_db)):
    try:
        session_id = request.headers.get("x-session-id")
        user_id = await auth_service.get_user_id(session_id)
        audio_service = AudioService(db)
        file_data = await file.read()
        return await audio_service.process_audio_message(user_id=user_id, file_data=file_data, file_name=file.filename)
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