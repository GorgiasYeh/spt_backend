from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from auth import verify_secret_key
from models import RequestModel, ResponseModel
from openai import OpenAI
from AIConfig import ai_config

router = APIRouter()

@router.post("/")
async def forward_request(request: Request):
    verify_secret_key(request)
    request_data = await request.json()
    request_model = RequestModel(**request_data)

    # 預設使用 XAI
    xai_config = ai_config.services.get("x-ai")
    if not xai_config:
        raise HTTPException(status_code=500, detail="x-ai 配置未找到")

    xai_client = OpenAI(
        api_key=xai_config.api_key,
        base_url=xai_config.base_url
    )

    try:
        completion = xai_client.beta.chat.completions.parse(
            model=xai_config.model,
            messages=[message.model_dump() for message in request_model.messages]
        )
        print(completion.model_dump())
        return JSONResponse(content=completion.model_dump())
    except Exception as e:
        # 如果 XAI 發生問題，使用 Gemini 備援
        gemini_config = ai_config.services.get("gemini")
        if not gemini_config:
            raise HTTPException(status_code=500, detail="Gemini 配置未找到")

        gemini_client = OpenAI(
            api_key=gemini_config.api_key,
            base_url=gemini_config.base_url
        )

        completion = gemini_client.beta.chat.completions.parse(
            model=gemini_config.model,
            messages=[message.model_dump() for message in request_model.messages]
        )
        return JSONResponse(content=completion.model_dump())

