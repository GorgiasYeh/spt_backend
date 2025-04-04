from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from auth import verify_secret_key
from models import RequestModel, ResponseModel
from openai import OpenAI
from AIConfig import ai_config
import logging

logger = logging.getLogger(__name__)

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

    try:
        if not xai_config.api_key:
            raise ValueError("API key is empty")
        
        logger.info(f"使用 base_url: {xai_config.base_url}")
        logger.info("API key 長度: " + str(len(xai_config.api_key)))
        
        xai_client = OpenAI(
            api_key=xai_config.api_key,
            base_url=xai_config.base_url
        )

        completion = xai_client.beta.chat.completions.parse(
            model=xai_config.model,
            messages=[message.model_dump() for message in request_model.messages]
        )
        print(completion.model_dump())
        return JSONResponse(content=completion.model_dump())
    except ValueError as ve:
        logger.error(f"設定錯誤: {str(ve)}")
        raise HTTPException(status_code=500, detail=str(ve))
    except Exception as e:
        logger.error(f"連接錯誤: {str(e)}")
        # raise HTTPException(status_code=500, detail="API 連接失敗")

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

@router.post("/stream")
async def forward_request_stream(request: Request):
    from fastapi.responses import StreamingResponse
    import json

    verify_secret_key(request)
    request_data = await request.json()
    request_model = RequestModel(**request_data)

    # 預設使用 XAI
    xai_config = ai_config.services.get("x-ai")
    if not xai_config:
        raise HTTPException(status_code=500, detail="x-ai 配置未找到")

    async def generate_stream():
        try:
            if not xai_config.api_key:
                raise ValueError("API key is empty")
            
            logger.info(f"使用 base_url: {xai_config.base_url}")
            logger.info("API key 長度: " + str(len(xai_config.api_key)))
            
            xai_client = OpenAI(
                api_key=xai_config.api_key,
                base_url=xai_config.base_url
            )

            # 使用串流模式獲取回應
            stream = xai_client.chat.completions.create(
                model=xai_config.model,
                messages=[message.model_dump() for message in request_model.messages],
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices and len(chunk.choices) > 0:
                    if chunk.choices[0].delta.content:
                        yield f"data: {json.dumps({'content': chunk.choices[0].delta.content})}\n\n"
            
            yield "data: [DONE]\n\n"
            
        except ValueError as ve:
            logger.error(f"設定錯誤: {str(ve)}")
            yield f"data: {json.dumps({'error': str(ve)})}\n\n"
        except Exception as e:
            logger.error(f"連接錯誤: {str(e)}")
            
            # 如果 XAI 發生問題，使用 Gemini 備援
            try:
                gemini_config = ai_config.services.get("gemini")
                if not gemini_config:
                    yield f"data: {json.dumps({'error': 'Gemini 配置未找到'})}\n\n"
                    return

                gemini_client = OpenAI(
                    api_key=gemini_config.api_key,
                    base_url=gemini_config.base_url
                )

                # 使用串流模式獲取 Gemini 回應
                stream = gemini_client.chat.completions.create(
                    model=gemini_config.model,
                    messages=[message.model_dump() for message in request_model.messages],
                    stream=True
                )
                
                for chunk in stream:
                    if chunk.choices and len(chunk.choices) > 0:
                        if chunk.choices[0].delta.content:
                            yield f"data: {json.dumps({'content': chunk.choices[0].delta.content})}\n\n"
                
                yield "data: [DONE]\n\n"
                
            except Exception as e2:
                logger.error(f"Gemini 備援也失敗: {str(e2)}")
                yield f"data: {json.dumps({'error': str(e2)})}\n\n"

    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream"
    )