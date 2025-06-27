from core.logger import setup_logger
from fastapi import APIRouter, Response, Request
import httpx
from fastapi.exceptions import HTTPException
from interfaces.text import text_interface
from interfaces.text_tasks import create_text_task, get_text_task_result

logger = setup_logger("routers.text")

router = APIRouter(
    prefix="/text",
    tags=["Text"]
)

async def _process_text_response(text_response: httpx.Response, response: Response):
    if "set-cookie" in text_response.headers:
        response.headers["set-cookie"] = text_response.headers["set-cookie"]
        logger.info("Установили куки в заголовки ответа")
    response_data = text_response.json()
    logger.info(f"Получили response_data = {response_data}")
    if text_response.is_error:
        detail = response_data.get("detail")
        if isinstance(detail, dict):
            logger.warning(f"Получили ошибку: detail = {detail}, status_code = {text_response.status_code}")
            raise HTTPException(
                status_code=text_response.status_code,
                detail={
                    "success": detail.get("success"),
                    "error": detail.get("error")
                }
            )
    return response_data

@router.post("/generate-answer")
async def generate_answer(request: Request, response: Response):
    try:
        logger.info("Получили запрос /generate-answer")
        session_id = request.cookies.get("sessionid")
        logger.info(f"Получили session_id = {session_id}")
        request_data = await request.json()
        logger.info(f"Получили request_data = {request_data}")
        text = request_data.get("text")
        logger.info(f"Получили text = {text}")
        task_id = await create_text_task(session_id, text)
        logger.info(f"Получили task_id = {task_id}")
        logger.info(f"Отправили в ответе task_id = {task_id}")
        return {"task_id": task_id}
    except Exception as e:
        logger.error(f"Ошибка создания задачи генерации текста: {str(e)}", exc_info=True)
        raise

@router.get("/tasks/{task_id}")
async def check_task_status(task_id: str):
    logger.info(f"Получили запрос /tasks/{task_id}")
    text_task_result = await get_text_task_result(task_id)
    logger.info(f"Получили text_task_result = {text_task_result}")
    logger.info(f"Отправили в ответе {text_task_result}")
    return text_task_result

@router.get("/get-text-messages")
async def get_text_messages(request: Request, response: Response):
    try:
        logger.info("Получили запрос /get-text-messages")
        headers = { "X-Session-ID": request.cookies.get("sessionid") }
        logger.info(f"Получили headers = {headers}")
        text_response = await text_interface.get_text_messages(headers)
        logger.info(f"Получили text_response = {text_response}")
        return await _process_text_response(text_response, response)
    except Exception as e:
        logger.error(f"Ошибка загрузки сообщений: {str(e)}", exc_info=True)
        raise

@router.delete("/delete-text-messages")
async def delete_text_messages(request: Request, response: Response):
    try:
        logger.info("Получили запрос /delete-text-messages")
        headers = { "X-Session-ID": request.cookies.get("sessionid") }
        logger.info(f"Получили headers = {headers}")
        text_response = await text_interface.delete_text_messages(headers)
        logger.info(f"Получили text_response = {text_response}")
        return await _process_text_response(text_response, response)
    except Exception as e:
        logger.error(f"Ошибка удаления сообщений: {str(e)}", exc_info=True)
        raise