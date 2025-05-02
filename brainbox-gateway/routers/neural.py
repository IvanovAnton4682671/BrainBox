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
        raise HTTPException(
            status_code=neural_response.status_code,
            detail={
                "success": detail.get("success"),
                "error": detail.get("error")
            }
        )
    return response_data

@router.post("/recognize-audio")
async def recognize_audio(file: UploadFile, request: Request, response: Response):
    headers = { "X-Session-ID": request.cookies.get("sessionid") }
    file_contents = await file.read()
    neural_response = await neural_service.recognize_audio(headers, file_contents, file.filename)
    return await _process_neural_response(neural_response, response)

@router.get("/get-audio-messages")
async def get_audio_messages(request: Request, response: Response):
    headers = { "X-Session-ID": request.cookies.get("sessionid") }
    neural_response = await neural_service.get_audio_messages(headers)
    return await _process_neural_response(neural_response, response)