from core.logger import setup_logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import audio
import uvicorn
from core.config import settings
import subprocess

logger = setup_logger("http")

app = FastAPI(
    title="BrainBox Neural Service",
    description="Сервис нейросетей проекта BrainBox"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(audio.router)

@app.get("/")
async def root():
    return {"message": "BrainBox Neural Service is running..."}

if __name__ == "__main__":
    subprocess.Popen(["dramatiq", "worker"])
    uvicorn.run("main:app", host=settings.NEURAL_HOST, port=settings.NEURAL_PORT, reload=True)