from fastapi import APIRouter
from fastapi import HTTPException
from schema import ChatRequest, ChatResponse
from agent import get_chat_response, build_graph
from utils import vector_store_path, web_name

chat_router = APIRouter(
    prefix="/chat", 
    tags=["Chat-bot"]
)


@chat_router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        graph=build_graph(vector_store_path=vector_store_path, web_name=web_name)
        final_response=await get_chat_response(graph=graph, question=request.message, thread_id=request.id)

        return ChatResponse(
            response=final_response
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))