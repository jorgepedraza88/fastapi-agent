from fastapi import APIRouter, HTTPException
from app.models import ChatRequest, ChatResponse, ChatMessage
from app.services.ollama_service import OllamaService

router = APIRouter()
ollama_service = OllamaService()


@router.post("/chat", response_model=ChatResponse)
async def ollama_chat(request: ChatRequest):
    """
    Send a chat completion request to Ollama API
    """
    try:
        response = await ollama_service.generate_chat_completion(
            messages=request.messages,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models")
async def get_models():
    """
    Get available Ollama models
    """
    try:
        models = await ollama_service.list_models()
        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
