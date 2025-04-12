from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ChatMessage(BaseModel):
    role: str = Field(...,
                      description="Role of the message sender (system, user, assistant)")
    content: str = Field(..., description="Content of the message")


class ChatRequest(BaseModel):
    messages: List[ChatMessage] = Field(...,
                                        description="List of messages in the conversation")
    model: str = Field(..., description="Model to use for the completion")
    temperature: Optional[float] = Field(
        0.7, description="Sampling temperature")
    max_tokens: Optional[int] = Field(
        1000, description="Maximum number of tokens to generate")


class ChatResponse(BaseModel):
    message: ChatMessage
    usage: Optional[Dict[str, int]] = None
    model: str
