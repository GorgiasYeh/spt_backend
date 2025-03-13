from dotenv import load_dotenv
import os
from fastapi import HTTPException, Request

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

def verify_secret_key(request: Request):
    secret_key = request.headers.get("secret_key")
    if secret_key != SECRET_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid secret key")
