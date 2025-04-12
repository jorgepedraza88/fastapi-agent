"""
OpenAI API Router
This module defines the FastAPI router for handling OpenAI API requests.
It includes endpoints for chat completions and model listing.
"""

import json
from typing import Dict, List
from fastapi import APIRouter, HTTPException, Request
from app.models import ChatResponse, ChatMessage
from app.services.openai_service import OpenAIService

router = APIRouter()
openai_service = OpenAIService()

# Diccionario para almacenar el historial de conversaciones en memoria
# En producción, esto debería ser una base de datos persistente
conversation_history: Dict[str, List[ChatMessage]] = {}


@router.post("/chat", response_model=ChatResponse)
async def openai_chat(request: Request):
    """
    Process a chat request and maintain conversation history
    """
    try:
        # Get the raw payload
        payload = await request.json()

        # Extract the message
        message_text = payload.get("message")
        if not message_text:
            raise HTTPException(status_code=400, detail="No message provided")

        # Extract the conversation_id (opcional)
        conversation_id = payload.get("conversation_id")

        # Create a proper ChatMessage object
        user_message = ChatMessage(role="user", content=message_text)

        # Default parameters
        model = payload.get("model", "gpt-4o-mini")
        temperature = payload.get("temperature", 0.7)
        max_tokens = payload.get("max_tokens", 1000)

        # Obtener el historial de la conversación si existe un ID
        history = None
        if conversation_id:
            history = conversation_history.get(conversation_id, [])

        # Se puede usar para limitar el numero de mensajes
        if history and len(history) > 3:
            print("La conversación tiene más de 3 mensajes")

        # Pass the message and history to the service
        response, updated_history = await openai_service.generate_chat_completion(
            messages=[user_message],
            history=history,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )

        # Guardar el historial actualizado si hay un ID de conversación
        if conversation_id:
            conversation_history[conversation_id] = updated_history

        # The service returns a ChatResponse object
        return response
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=400, detail="Invalid JSON payload") from exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/history/{conversation_id}")
async def get_conversation_history(conversation_id: str):
    """
    Get the history of a specific conversation
    """
    if conversation_id not in conversation_history:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Devolver los mensajes de la conversación
    messages = conversation_history[conversation_id]
    return {
        "conversation_id": conversation_id,
        "messages": messages,
        "message_count": len(messages)
    }
