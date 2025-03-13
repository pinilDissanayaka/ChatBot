from fastapi import APIRouter
from fastapi import HTTPException
from schema import ChatRequest, ChatResponse
from agent import get_chat_response, build_graph


chat_router = APIRouter(
    prefix="/chat", 
    tags=["Chat-bot"]
)


@chat_router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        graph=build_graph(web_name=request.name)
        final_response=await get_chat_response(graph=graph, question=request.message, thread_id=request.thread_id)

        return ChatResponse(
            response=final_response
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))