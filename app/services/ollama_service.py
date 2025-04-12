"""Este módulo define a classe OllamaService, que se conecta a la API de Ollama"""

import os
from typing import List, Optional
import httpx
from app.models import ChatMessage, ChatResponse


class OllamaService:
    """
    OllamaService is a service class that interacts with the Ollama API
    to generate chat completions. It handles the API requests and responses,
    and formats the data accordingly.
    """

    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

        # Default models - these would normally be fetched from the API
        self.default_models = [
            "llama3",
            "mistral",
            "gemma",
            "falcon",
            "phi3"
        ]

    async def generate_chat_completion(
        self,
        messages: List[ChatMessage],
        model: str = "llama3",
        temperature: Optional[float] = 0.7,
        max_tokens: Optional[int] = 1000
    ) -> ChatResponse:
        """
        Generate a chat completion using Ollama API
        """
        # Format messages for Ollama API
        # Ollama's API is a bit different from OpenAI's
        # We need to convert our messages to Ollama's format

        # Create payload for Ollama API
        payload = {
            "model": model,
            "messages": [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ],
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            }
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                    timeout=60.0  # Longer timeout for model inference
                )
                response.raise_for_status()
                result = response.json()

                # Extract the response content
                assistant_message = ChatMessage(
                    role="assistant",
                    content=result.get("message", {}).get("content", "")
                )

                # Create our response object
                return ChatResponse(
                    message=assistant_message,
                    # Ollama doesn't provide token usage in the same way as OpenAI
                    usage=None,
                    model=model
                )
        except httpx.RequestError as e:
            raise Exception(
                f"Error communicating with Ollama API: {str(e)}") from e
        except httpx.HTTPStatusError as e:
            raise Exception(
                f"Ollama API returned error {e.response.status_code}: {e.response.text}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
