from core.logger import setup_logger
from fastapi import APIRouter, UploadFile, Request, Response
import httpx
from interfaces.neural import neural_service
from fastapi.exceptions import HTTPException

logger = setup_logger("routers/neural.py")

router = APIRouter(
    prefix="/neural",
    tags=["Neural"]
)

async def _process_neural_response(neural_response: httpx.Response, response: Response):
    #устанавливаем куки, если они есть
    if "set-cookie" in neural_response.headers:
        response.headers["set-cookie"] = neural_response.headers["set-cookie"]
    response_data = neural_response.json() #получаем данные как есть
    #если есть ошибка - возвращаем её как есть
    if neural_response.is_error:
        detail = response_data.get("detail")
        print(detail)
        if isinstance(detail, dict):
            raise HTTPException(
                status_code=neural_response.status_code,
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
    neural_response = await neural_service.upload_audio(headers, file_contents, file.filename)
    return await _process_neural_response(neural_response, response)

@router.post("/recognize-saved-audio")
async def recognize_saved_audio(request: Request, response: Response):
    headers = { "X-Session-ID": request.cookies.get("sessionid") }
    request_data = await request.json()
    audio_uid = request_data.get("audio_uid")
    neural_response = await neural_service.recognize_saved_audio(headers, audio_uid)
    return await _process_neural_response(neural_response, response)

@router.get("/get-audio-messages")
async def get_audio_messages(request: Request, response: Response):
    headers = { "X-Session-ID": request.cookies.get("sessionid") }
    neural_response = await neural_service.get_audio_messages(headers)
    return await _process_neural_response(neural_response, response)

@router.get("/download-audio/{audio_uid}")
async def download_audio(request: Request, audio_uid: str, response: Response):
    headers = { "X-Session-ID": request.cookies.get("sessionid") }
    neural_response = await neural_service.download_audio(headers, audio_uid)
    return Response(
        content=neural_response.content,
        media_type=neural_response.headers.get("content-type", "audio/mpeg"),
        headers=dict(neural_response.headers)
    )