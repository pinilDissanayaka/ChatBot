from fastapi import APIRouter
from fastapi import HTTPException
from schema import ChatRequest, ChatResponse
from agent import get_chat_response, build_graph
from functools import lru_cache



chat_router = APIRouter(
    prefix="/chat", 
    tags=["Chat-bot"]
)



@lru_cache(maxsize=200)
def get_cached_graph(web_name: str):
    return build_graph(web_name=web_name)



@chat_router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a chat request and return a streaming response."""
    try:
        graph = get_cached_graph(web_name=request.name)
        
        return ChatResponse(
            response=await get_chat_response(graph=graph, question=request.message, thread_id=request.thread_id)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")