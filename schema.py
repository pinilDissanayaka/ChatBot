from pydantic import BaseModel

class ChatRequest(BaseModel):
    id: str = "1"
    message: str = "Hello"
    

class ChatResponse(BaseModel):
    response: str