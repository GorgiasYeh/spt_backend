import os
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from auth import verify_secret_key
from models import RequestModel, ResponseModel
from openai import OpenAI

router = APIRouter()

@router.post("/")
async def forward_request(request: Request):
    verify_secret_key(request)
    request_data = await request.json()
    request_model = RequestModel(**request_data)

    client = OpenAI(api_key=os.getenv("API_KEY"), base_url=request_model.base_url)
    completion = client.beta.chat.completions.parse(
        model=request_model.model,
        messages=[message.model_dump() for message in request_model.messages],
        # response_format=ResponseModel
    )

    # improvement_result = completion.choices[0].message.parsed
    # return JSONResponse(content=improvement_result.model_dump())
    return JSONResponse(content=completion.model_dump())
