from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.logger import setup_logger
from routers import auth, neural
from core.task_listener import start_listener_in_background
import uvicorn

logger = setup_logger("http")

app = FastAPI(
    title="BrainBox API Gateway",
    description="API Gateway-узел проекта BrainBox"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CLIENT_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(neural.router)

@app.get("/")
async def root():
    return {"message": "BrainBox API Gateway is running..."}

if __name__ == "__main__":
    logger.info("API Gateway запущен!")
    uvicorn.run("main:app", host=settings.GATEWAY_HOST, port=settings.GATEWAY_PORT, reload=True)
    start_listener_in_background()