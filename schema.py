from pydantic import BaseModel
from typing import List
from fastapi import UploadFile

class ChatRequest(BaseModel):
    thread_id: str = "1"
    name: str
    message: str = "Hello"
    

class ChatResponse(BaseModel):
    response: str
    
    