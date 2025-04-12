"""OpenAI Service Module"""

import os
from typing import List, Optional
from openai import AsyncOpenAI
from app.models import ChatMessage, ChatResponse


class OpenAIService:
    """
    OpenAIService is a service class that interacts with the OpenAI API
    to generate chat completions. It handles the API requests and responses,
    and formats the data accordingly.
    """

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        # Solo inicializar el cliente si hay una clave de API
        self.client = None
        if self.api_key:
            self.client = AsyncOpenAI(api_key=self.api_key)

        # Default models - these would normally be fetched from the API
        self.default_models = [
            "gpt-4o-mini"
        ]

    async def generate_chat_completion(
        self,
        messages: List[ChatMessage],
        model: str = "gpt-4o-mini",
        temperature: Optional[float] = 0.7,
        max_tokens: Optional[int] = 1000
    ) -> ChatResponse:
        """
        Generate a chat completion using OpenAI API
        """
        if not self.client:
            raise ImportError(
                "OpenAI API key is not configured. Please set the OPENAI_API_KEY environment variable.")

        # Convert our ChatMessage objects to the format OpenAI expects
        openai_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

        response = await self.client.chat.completions.create(
            model=model,
            messages=openai_messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        # Extract the response content
        assistant_message = ChatMessage(
            role="assistant",
            content=response.choices[0].message.content
        )

        # Create our response object
        return ChatResponse(
            message=assistant_message,
            usage={
                "completion_tokens": response.usage.completion_tokens,
                "prompt_tokens": response.usage.prompt_tokens,
                "total_tokens": response.usage.total_tokens
            },
            model=model
        )
