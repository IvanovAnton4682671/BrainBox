from core.logger import setup_logger
from fastapi import APIRouter, UploadFile, Request, Response
import httpx
from interfaces.audio import audio_interface
from fastapi.exceptions import HTTPException
from interfaces.audio_tasks import create_audio_task, get_audio_task_result

logger = setup_logger("routers/audio.py")

router = APIRouter(
    prefix="/audio",
    tags=["Audio"]
)

async def _process_audio_response(audio_response: httpx.Response, response: Response):
    #устанавливаем куки, если они есть
    if "set-cookie" in audio_response.headers:
        response.headers["set-cookie"] = audio_response.headers["set-cookie"]
    response_data = audio_response.json() #получаем данные как есть
    #если есть ошибка - возвращаем её как есть
    if audio_response.is_error:
        detail = response_data.get("detail")
        if isinstance(detail, dict):
            raise HTTPException(
                status_code=audio_response.status_code,
                detail={
                    "success": detail.get("success"),
                    "error": detail.get("error")
                }
            )
    return response_data

@router.post("/upload-audio")
async def upload_audio(file: UploadFile, request: Request, response: Response):
    headers = { "X-Session-ID": request.cookies.get("sessionid") }
    file_contents = await file.read()
    audio_response = await audio_interface.upload_audio(headers, file_contents, file.filename)
    return await _process_audio_response(audio_response, response)

@router.post("/recognize-saved-audio")
async def recognize_saved_audio(request: Request, response: Response):
    session_id = request.cookies.get("sessionid")
    request_data = await request.json()
    audio_uid = request_data.get("audio_uid")
    task_id = await create_audio_task(session_id, audio_uid)
    return { "task_id": task_id }

@router.get("/tasks/{task_id}")
async def check_task_status(task_id: str):
    return await get_audio_task_result(task_id)

@router.get("/get-audio-messages")
async def get_audio_messages(request: Request, response: Response):
    headers = { "X-Session-ID": request.cookies.get("sessionid") }
    audio_response = await audio_interface.get_audio_messages(headers)
    return await _process_audio_response(audio_response, response)

@router.get("/download-audio/{audio_uid}")
async def download_audio(request: Request, audio_uid: str, response: Response):
    headers = { "X-Session-ID": request.cookies.get("sessionid") }
    audio_response = await audio_interface.download_audio(headers, audio_uid)
    return Response(
        content=audio_response.content,
        media_type=audio_response.headers.get("content-type", "audio/mpeg"),
        headers=dict(audio_response.headers)
    )

@router.delete("/delete-audio-messages")
async def delete_audio_messages(request: Request, response: Response):
    headers = { "X-Session-ID": request.cookies.get("sessionid") }
    audio_response = await audio_interface.delete_audio_messages(headers)
    return await _process_audio_response(audio_response, response)