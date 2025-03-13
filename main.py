from fastapi import FastAPI, Request
from proxy import router as proxy_router
import logging
from datetime import datetime
import socket

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# 診斷中間件
@app.middleware("http")
async def diagnose_requests(request: Request, call_next):
    logger.info(f"收到請求: {request.method} {request.url}")
    logger.info(f"客戶端 IP: {request.client.host if request.client else 'unknown'}")
    logger.info(f"Headers: {request.headers}")
    response = await call_next(request)
    return response

app.include_router(proxy_router, prefix="/proxy")

@app.get("/")
async def root():
    hostname = socket.gethostname()
    return {
        "message": "Hello World",
        "hostname": hostname,
        "timestamp": datetime.now().isoformat(),
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "hostname": socket.gethostname()
    }