from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.routers import authentication
import uvicorn
from core.logger import setup_logger
import time
from databases.redis import redis

logger = setup_logger("http")

app = FastAPI(
    title="BrainBox Authentication Service",
    description="Сервис аутентификации пользователей проекта BrainBox"
)

#настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#подключение роутера
app.include_router(authentication.router)

@app.middleware("http")
async def log_request(request: Request, call_next):
    """
    Метод для логирования всех http-запросов
    """
    start_time = time.time()
    logger.info(f"Attempt request: {request.method} {request.url}")
    try:
        sessionid = request.cookies.get("sessionid")
        if sessionid:
            user_id = await redis.get(f"session:{sessionid}")
            if not user_id:
                response = Response(status_code=401)
                response.delete_cookie("sessionid")
                process_time = (time.time() - start_time) * 1000
                logger.warning(
                    f"Invalid session: {request.method} {request.url}"
                    f" Status: {response.status_code}"
                    f" Time: {process_time:.2f}ms"
                )
                return response
            request.state.user_id = int(user_id)
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logger.info(
            f"Response: {request.method} {request.url}"
            f" Status: {response.status_code}"
            f" Time: {process_time:.2f}ms"
        )
        return response
    except Exception as e:
        process_time = (time.time() - start_time) * 1000
        logger.error(
            f"Request failed: {request.method} {request.url}"
            f" Error: {str(e)}"
            f" Time: {process_time:.2f}ms",
            exc_info=True
        )
        if isinstance(e, HTTPException) and e.status_code == 401:
            response = Response(
                content=f"Auth error: {str(e)}",
                status_code=401
            )
            response.delete_cookie("sessionid")
            return response
        return Response(
            content=f"Internal server error: {str(e)}",
            status_code=500
        )

@app.get("/")
async def root():
    return {"message": "BrainBox Authentication Service is running..., for help: http://localhost:8001/docs"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8001, reload=True)