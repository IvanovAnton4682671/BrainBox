from core.logger import setup_logger
from fastapi import APIRouter, Request, Response
import httpx
from fastapi.exceptions import HTTPException
from interfaces.image import image_interface
from interfaces.image_tasks import create_image_task, get_image_task_result

logger = setup_logger("routers/image.py")

router = APIRouter(
    prefix="/image",
    tags=["Image"]
)

async def _process_image_response(image_response: httpx.Response, response: Response):
    if "set-cookie" in image_response.headers:
        response.headers["set-cookie"] = image_response.headers["set-cookie"]
    response_data = image_response.json()
    if image_response.is_error:
        detail = response_data.get("detail")
        if isinstance(detail, dict):
            raise HTTPException(
                status_code=image_response.status_code,
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
        task_id = await create_image_task(session_id, text)
        return {"task_id": task_id}
    except Exception as e:
        logger.error(f"Ошибка генерации ответа: {str(e)}", exc_info=True)
        raise

@router.get("/tasks/{task_id}")
async def check_task_status(task_id: str):
    return await get_image_task_result(task_id)

@router.get("/view/{image_uid}")
async def view_image(request: Request, response: Response, image_uid: str):
    try:
        headers = {"X-Session-ID": request.cookies.get("sessionid")}
        image_response = await image_interface.view_image(headers, image_uid)
        return Response(
            content=image_response.content,
            media_type=image_response.headers.get("content-type", "image/jpeg"),
            headers=dict(image_response.headers)
        )
    except Exception as e:
        logger.error(f"Ошибка отображения картинки: {str(e)}", exc_info=True)
        raise

@router.get("/download/{image_uid}")
async def download_image(request: Request, response: Response, image_uid: str):
    try:
        headers = {"X-Session-ID": request.cookies.get("sessionid")}
        image_response = await image_interface.download_image(headers, image_uid)
        return Response(
            content=image_response.content,
            media_type=image_response.headers.get("content-type", "image/jpeg"),
            headers=dict(image_response.headers)
        )
    except Exception as e:
        logger.error(f"Ошибка загрузки картинки: {str(e)}", exc_info=True)
        raise

@router.get("/get-image-messages")
async def get_image_messages(request: Request, response: Response):
    try:
        headers = {"X-Session-ID": request.cookies.get("sessionid")}
        image_response = await image_interface.get_image_messages(headers)
        return await _process_image_response(image_response, response)
    except Exception as e:
        logger.error(f"Ошибка получения истории чата: {str(e)}", exc_info=True)
        raise

@router.delete("/delete-image-messages")
async def delete_image_messages(request: Request, response: Response):
    try:
        headers = {"X-Session-ID": request.cookies.get("sessionid")}
        image_response = await image_interface.delete_image_messages(headers)
        return await _process_image_response(image_response, response)
    except Exception as e:
        logger.error(f"Ошибка удаления истории чата: {str(e)}", exc_info=True)
        raise