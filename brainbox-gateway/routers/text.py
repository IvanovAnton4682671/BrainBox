from core.logger import setup_logger
from fastapi import APIRouter, Response, Request
import httpx
from fastapi.exceptions import HTTPException
from interfaces.text import text_interface
from interfaces.text_tasks import create_text_task, get_text_task_result

logger = setup_logger("routers/text.py")

router = APIRouter(
    prefix="/text",
    tags=["Text"]
)

async def _process_text_response(text_response: httpx.Response, response: Response):
    if "set-cookie" in text_response.headers:
        response.headers["set-cookie"] = text_response.headers["set-cookie"]
    response_data = text_response.json()
    if text_response.is_error:
        detail = response_data.get("detail")
        if isinstance(detail, dict):
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
        session_id = request.cookies.get("sessionid")
        request_data = await request.json()
        text = request_data.get("text")
        task_id = await create_text_task(session_id, text)
        return {"task_id": task_id}
    except Exception as e:
        logger.error(f"Ошибка генерации ответа: {str(e)}", exc_info=True)
        raise

@router.get("/tasks/{task_id}")
async def check_task_status(task_id: str):
    return await get_text_task_result(task_id)

@router.get("/get-text-messages")
async def get_text_messages(request: Request, response: Response):
    try:
        headers = { "X-Session-ID": request.cookies.get("sessionid") }
        text_response = await text_interface.get_text_messages(headers)
        return await _process_text_response(text_response, response)
    except Exception as e:
        logger.error(f"Ошибка загрузки сообщений: {str(e)}", exc_info=True)
        raise

@router.delete("/delete-text-messages")
async def delete_text_messages(request: Request, response: Response):
    try:
        headers = { "X-Session-ID": request.cookies.get("sessionid") }
        text_response = await text_interface.delete_text_messages(headers)
        return await _process_text_response(text_response, response)
    except Exception as e:
        logger.error(f"Ошибка удаления сообщений: {str(e)}", exc_info=True)
        raise