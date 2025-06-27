from core.logger import setup_logger
from fastapi import APIRouter, Request, Response
import httpx
from fastapi.exceptions import HTTPException
from interfaces.image import image_interface
from interfaces.image_tasks import create_image_task, get_image_task_result

logger = setup_logger("routers.image")

router = APIRouter(
    prefix="/image",
    tags=["Image"]
)

async def _process_image_response(image_response: httpx.Response, response: Response):
    if "set-cookie" in image_response.headers:
        response.headers["set-cookie"] = image_response.headers["set-cookie"]
        logger.info("Установили куки в заголовки ответа")
    response_data = image_response.json()
    logger.info(f"Получили response_data = {response_data}")
    if image_response.is_error:
        detail = response_data.get("detail")
        if isinstance(detail, dict):
            logger.warning(f"Получили ошибку: detail = {detail}, status_code = {image_response.status_code}")
            raise HTTPException(
                status_code=image_response.status_code,
                detail={
                    "success": detail.get("success"),
                    "error": detail.get("error")
                }
            )
    logger.info(f"Отправили в ответе response_data = {response_data}")
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
        task_id = await create_image_task(session_id, text)
        logger.info(f"Получили task_id = {task_id}")
        logger.info(f"Отправили в ответе task_id = {task_id}")
        return {"task_id": task_id}
    except Exception as e:
        logger.error(f"Ошибка создания задачи генерации картинки: {str(e)}", exc_info=True)
        raise

@router.get("/tasks/{task_id}")
async def check_task_status(task_id: str):
    logger.info(f"Получили запрос /tasks/{task_id}")
    image_task_result = await get_image_task_result(task_id)
    logger.info(f"Получили image_task_result = {image_task_result}")
    logger.info(f"Отправили в ответе {image_task_result}")
    return image_task_result

@router.get("/view/{image_uid}")
async def view_image(request: Request, response: Response, image_uid: str):
    try:
        logger.info(f"Получили запрос /view/{image_uid}")
        headers = {"X-Session-ID": request.cookies.get("sessionid")}
        logger.info(f"Получили headers = {headers}")
        image_response = await image_interface.view_image(headers, image_uid)
        logger.info(f"Получили image_response = {image_response}")
        logger.info(f"Отправили в ответе Response с полями: content = *тут оч много всего*, media_type = image/jpeg, headers = {dict(image_response.headers)}")
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
        logger.info(f"Получили запрос /download/{image_uid}")
        headers = {"X-Session-ID": request.cookies.get("sessionid")}
        logger.info(f"Получили headers = {headers}")
        image_response = await image_interface.download_image(headers, image_uid)
        logger.info(f"Получили image_response = {image_response}")
        logger.info(f"Отправили в ответе Response с полями: content = *тут оч много всего*, media_type = image/jpeg, headers = {dict(image_response.headers)}")
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
        logger.info("Получили запрос /get-image-messages")
        headers = {"X-Session-ID": request.cookies.get("sessionid")}
        logger.info(f"Получили headers = {headers}")
        image_response = await image_interface.get_image_messages(headers)
        logger.info(f"Получили image_response = {image_response}")
        return await _process_image_response(image_response, response)
    except Exception as e:
        logger.error(f"Ошибка получения истории чата: {str(e)}", exc_info=True)
        raise

@router.delete("/delete-image-messages")
async def delete_image_messages(request: Request, response: Response):
    try:
        logger.info("Получили запрос /delete-image-messages")
        headers = {"X-Session-ID": request.cookies.get("sessionid")}
        logger.info(f"Получили headers = {headers}")
        image_response = await image_interface.delete_image_messages(headers)
        logger.info(f"Получили image_response = {image_response}")
        return await _process_image_response(image_response, response)
    except Exception as e:
        logger.error(f"Ошибка удаления истории чата: {str(e)}", exc_info=True)
        raise