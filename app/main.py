from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Verificar variables de entorno críticas
if not os.getenv("OPENAI_API_KEY"):
    logger.warning("OPENAI_API_KEY no está configurada. Las funciones de OpenAI no estarán disponibles.")

# Importar routers
from app.routers import openai_router, ollama_router

# Create FastAPI app
app = FastAPI(
    title="AI API Service",
    description="API service for interacting with AI models through OpenAI and Ollama",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(openai_router.router, prefix="/api/openai", tags=["OpenAI"])
app.include_router(ollama_router.router, prefix="/api/ollama", tags=["Ollama"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to AI API Service",
        "docs": "/docs",
        "endpoints": ["/api/openai", "/api/ollama"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
