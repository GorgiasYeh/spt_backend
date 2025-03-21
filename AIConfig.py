import os
from pydantic import BaseModel
from typing import Dict, List

class AIServiceConfig(BaseModel):
    api_key: str
    base_url: str
    model: str

class AIConfig(BaseModel):
    services: Dict[str, AIServiceConfig]

# AI 服務配置
ai_config = AIConfig(
    services={
        "x-ai": AIServiceConfig(
            api_key=os.getenv("XAI_API_KEY", ""),
            base_url="https://api.x-ai.com/v1",
            model="x-model-v1"
        ),
        "gemini": AIServiceConfig(
            api_key=os.getenv("GEMINI_API_KEY", ""),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            model="gemini-2.0-flash-exp-image-generation"
        )
    }
)