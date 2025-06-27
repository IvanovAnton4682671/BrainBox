from core.logger import setup_logger
from fastapi import APIRouter, UploadFile, Request, Response
import httpx
from interfaces.audio import audio_interface
from fastapi.exceptions import HTTPException
from interfaces.audio_tasks import create_audio_task, get_audio_task_result

logger = setup_logger("routers.audio")

router = APIRouter(
    prefix="/audio",
    tags=["Audio"]
)

async def _process_audio_response(audio_response: httpx.Response, response: Response):
    #устанавливаем куки, если они есть
    if "set-cookie" in audio_response.headers:
        response.headers["set-cookie"] = audio_response.headers["set-cookie"]
        logger.info("Установили куки в заголовки ответа")
    response_data = audio_response.json() #получаем данные как есть
    logger.info(f"Получили response_data = {response_data}")
    #если есть ошибка - возвращаем её как есть
    if audio_response.is_error:
        detail = response_data.get("detail")
        if isinstance(detail, dict):
            logger.warning(f"Получили ошибку: detail = {detail}, status_code = {audio_response.status_code}")
            raise HTTPException(
                status_code=audio_response.status_code,
                detail={
                    "success": detail.get("success"),
                    "error": detail.get("error")
                }
            )
    logger.info(f"Отправили в ответе response_data = {response_data}")
    return response_data

@router.post("/upload-audio")
async def upload_audio(file: UploadFile, request: Request, response: Response):
    logger.info("Получили запрос /upload-audio")
    headers = { "X-Session-ID": request.cookies.get("sessionid") }
    logger.info(f"Получили headers = {headers}")
    file_contents = await file.read()
    logger.info("Получили file_content = *поток-байтов*")
    audio_response = await audio_interface.upload_audio(headers, file_contents, file.filename)
    logger.info(f"Получили audio_response = {audio_response}")
    return await _process_audio_response(audio_response, response)

@router.post("/recognize-saved-audio")
async def recognize_saved_audio(request: Request, response: Response):
    logger.info("Получили запрос /recognize-saved-audio")
    session_id = request.cookies.get("sessionid")
    logger.info(f"Получили session_id = {session_id}")
    request_data = await request.json()
    logger.info(f"Получили request_data = {request_data}")
    audio_uid = request_data.get("audio_uid")
    logger.info(f"Получили audio_uid = {audio_uid}")
    task_id = await create_audio_task(session_id, audio_uid)
    logger.info(f"Получили task_id = {task_id}")
    logger.info(f"Отправили в ответе task_id = {task_id}")
    return { "task_id": task_id }

@router.get("/tasks/{task_id}")
async def check_task_status(task_id: str):
    logger.info(f"Получили запрос /tasks/{task_id}")
    audio_task_result = await get_audio_task_result(task_id)
    logger.info(f"Получили audio_task_result = {audio_task_result}")
    logger.info(f"Отправили в ответе {audio_task_result}")
    return audio_task_result

@router.get("/get-audio-messages")
async def get_audio_messages(request: Request, response: Response):
    logger.info(f"Пришёл запрос /get-audio-messages")
    headers = { "X-Session-ID": request.cookies.get("sessionid") }
    logger.info(f"Получили headers = {headers}")
    audio_response = await audio_interface.get_audio_messages(headers)
    logger.info(f"Получили audio_response = {audio_response}")
    return await _process_audio_response(audio_response, response)

@router.get("/download-audio/{audio_uid}")
async def download_audio(request: Request, audio_uid: str, response: Response):
    logger.info(f"Получили запрос /download-audio/{audio_uid}")
    headers = { "X-Session-ID": request.cookies.get("sessionid") }
    logger.info(f"Получили headers = {headers}")
    audio_response = await audio_interface.download_audio(headers, audio_uid)
    logger.info(f"Получили audio_response = {audio_response}")
    logger.info(f"Отправили в ответе Response с полями: content = {audio_response.content}, media_type = audio/mpeg, headers = {dict(audio_response.headers)}")
    return Response(
        content=audio_response.content,
        media_type=audio_response.headers.get("content-type", "audio/mpeg"),
        headers=dict(audio_response.headers)
    )

@router.delete("/delete-audio-messages")
async def delete_audio_messages(request: Request, response: Response):
    logger.info("Получили запрос /delete-audio-messages")
    headers = { "X-Session-ID": request.cookies.get("sessionid") }
    logger.info(f"Получили headers = {headers}")
    audio_response = await audio_interface.delete_audio_messages(headers)
    logger.info(f"Получили audio_response = {audio_response}")
    return await _process_audio_response(audio_response, response)