from fastapi import FastAPI
from proxy import router as proxy_router

app = FastAPI()

app.include_router(proxy_router, prefix="/proxy")
