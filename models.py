from pydantic import BaseModel, Field
from typing import List

class ImproverPrompt(BaseModel):
    content: str = Field(description="Text to be improved")

class ListImproverPrompt(BaseModel):
    messages: List[ImproverPrompt]

class Message(BaseModel):
    role: str = Field(description="Role of the message sender")
    content: str = Field(description="Content of the message")

class RequestModel(BaseModel):
    base_url: str
    model: str
    messages: List[Message]

class ResponseModel(BaseModel):
    improvement_result: List[ImproverPrompt]
