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
    """Fetches a graph from cache, or builds it if it doesn't exist
    
    Args:
        web_name (str): The name of the website for which to build the graph
    
    Returns:
        StateGraph: A graph representing the state machine
    """
    
    return build_graph(web_name=web_name)



@chat_router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Responds to a user's question using the chatbot state machine
    """
    try:
        graph = get_cached_graph(web_name=request.name)
        
        return ChatResponse(
            response=await get_chat_response(graph=graph, question=request.message, thread_id=request.thread_id)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")