from core.logger import setup_logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import audio, text, image
import uvicorn
from core.config import settings
import multiprocessing
import sys
import time
from prometheus_fastapi_instrumentator import Instrumentator

logger = setup_logger("main")

app = FastAPI(
    title="BrainBox Neural Service",
    description="Сервис нейросетей проекта BrainBox"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.GATEWAY_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(audio.router)
app.include_router(image.router)
app.include_router(text.router)

@app.get("/")
async def root():
    return {"message": "BrainBox Neural Service is running..."}

Instrumentator().instrument(app).expose(app)

def run_worker():
    """
    Запускает воркер в отдельном потоке
    """

    from dramatiq.cli import main as dramatiq_main
    logger.info("Запускаем dramatiq worker в параллельных процессах")
    processes = multiprocessing.cpu_count()
    sys.argv = [
        "dramatiq",
        "worker",
        "--processes", f"{processes}",
        "--threads", "1"
    ]
    dramatiq_main()

def run_server():
    """
    Запускает сервер
    """

    logger.info("Сервис нейросетей запущен...")
    uvicorn.run(
        "main:app",
        host=settings.NEURAL_HOST,
        port=settings.NEURAL_PORT,
        reload=True
    )

if __name__ == "__main__":
    time.sleep(30)
    worker_process = multiprocessing.Process(target=run_worker)
    worker_process.start()
    try:
        run_server()
    except KeyboardInterrupt:
        logger.info("Получен сигнал прерывания, процессы завершаются...")
    finally:
        logger.info("Останавливаем воркер...")
        worker_process.terminate()
        worker_process.join(timeout=5)
        if worker_process.is_alive():
            logger.warning("Воркер не завершился корректно, принудительное завершение...")
            worker_process.kill()
        logger.info("Все процессы остановлены.")