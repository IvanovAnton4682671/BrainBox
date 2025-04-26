from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.logger import setup_logger
from routers import auth
import uvicorn

logger = setup_logger("http")

app = FastAPI(
    title="BrainBox API Gateway",
    description="API Gateway-узел проекта BrainBox"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "BrainBox API Gateway is running..., for help http://localhost:8000/docs"}

if __name__ == "__main__":
    logger.info("API Gateway запущен!")
    uvicorn.run("main:app", host=settings.GATEWAY_HOST, port=settings.GATEWAY_PORT, reload=True)