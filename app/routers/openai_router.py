"""
OpenAI API Router
This module defines the FastAPI router for handling OpenAI API requests.
It includes endpoints for chat completions and model listing.
"""

from fastapi import APIRouter, HTTPException, Request
from app.models import ChatResponse, ChatMessage
from app.services.openai_service import OpenAIService
import json

router = APIRouter()
openai_service = OpenAIService()


@router.post("/chat", response_model=ChatResponse)
async def openai_chat(request: Request):
    """
    Process a chat request containing only a message field
    """
    try:
        # Get the raw payload
        payload = await request.json()

        # Extract the message
        message_text = payload.get("message")

        if not message_text:
            raise HTTPException(status_code=400, detail="No message provided")

        # Create a proper ChatMessage object
        user_message = ChatMessage(role="user", content=message_text)

        # Default parameters
        model = "gpt-4o-mini"
        temperature = 0.7
        max_tokens = 1000

        # Pass a list of ChatMessage objects to the service
        response = await openai_service.generate_chat_completion(
            messages=[user_message],
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )

        # The service already returns a ChatResponse object
        return response
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
