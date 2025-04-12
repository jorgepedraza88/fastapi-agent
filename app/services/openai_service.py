"""OpenAI Service Module"""

import os
from typing import List, Optional, Tuple
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
        messages: List[ChatMessage],  # Lista de mensajes recibidos del cliente
        # Historial de mensajes previos (opcional)
        history: Optional[List[ChatMessage]] = None,
        model: str = "gpt-4o-mini",   # Modelo a usar, con valor por defecto
        # Controla la aleatoriedad de las respuestas
        temperature: Optional[float] = 0.7,
        max_tokens: Optional[int] = 1000  # Longitud máxima de la respuesta
    ) -> Tuple[ChatResponse, List[ChatMessage]]:  # Devuelve la respuesta y el historial actualizado
        """
        Generate a chat completion using OpenAI API and manage conversation history
        """
        # PASO 0: Inicializar el historial si no se proporciona
        if history is None:
            history = []

        # PASO 1: Verificar si tenemos un cliente de OpenAI inicializado
        if not self.client:
            raise ImportError(
                "OpenAI API key is not configured. Please set the OPENAI_API_KEY environment variable.")

        # PASO 2: Crear un mensaje de sistema predeterminado
        system_message_content = "Eres un asistente útil que ayuda a los usuarios a encontrar información y resolver problemas. "
        system_message_content += "Utilizas un tono humorístico y sarcástico, pero siempre manteniendo la amabilidad y el respeto. "
        system_message_content += "Tu respuestas no deben tener más de una oración."

        system_message = ChatMessage(
            role="system",
            content=system_message_content
        )

        # PASO 3: Combinar historial con nuevos mensajes
        all_user_messages = history + messages

        # PASO 4: Añadir el mensaje de sistema al principio de todos los mensajes
        all_messages = [system_message] + all_user_messages

        # PASO 5: Convertir nuestros objetos ChatMessage al formato que espera la API de OpenAI
        openai_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in all_messages
        ]

        # PASO 6: Hacer la llamada a la API de OpenAI
        response = await self.client.chat.completions.create(
            model=model,
            messages=openai_messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        # PASO 7: Extraer el contenido de la respuesta
        assistant_message = ChatMessage(
            role="assistant",
            content=response.choices[0].message.content
        )

        # PASO 8: Actualizar el historial con los nuevos mensajes y la respuesta
        updated_history = all_user_messages + [assistant_message]

        # PASO 9: Crear nuestro objeto de respuesta
        chat_response = ChatResponse(
            message=assistant_message,
            usage={
                "completion_tokens": response.usage.completion_tokens,
                "prompt_tokens": response.usage.prompt_tokens,
                "total_tokens": response.usage.total_tokens
            },
            model=model
        )

        # PASO 10: Devolver tanto la respuesta como el historial actualizado
        return chat_response, updated_history
