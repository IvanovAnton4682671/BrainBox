from core.logger import setup_logger
from fastapi import APIRouter, UploadFile
from tempfile import NamedTemporaryFile
from services.audio import recognize_audio
import os

logger = setup_logger("api/routers/neural.py")

router = APIRouter(
    prefix="/neural",
    tags=["Neural"]
)

@router.post("/recognize-audio")
async def process_audio(file: UploadFile):
    try:
        with NamedTemporaryFile(delete=False, suffix=f".{file.filename.split(".")[-1]}") as temp_audio:
            content = await file.read()
            temp_audio.write(content)
            temp_path = temp_audio.name
        result = recognize_audio(temp_path)
        os.unlink(temp_path)
        return result
    except Exception as e:
        raise e