"""
LangChain RAG Assistant - FastAPI Backend

A RAG-powered assistant for LangChain, LangGraph, and LangSmith documentation.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from routers import chat_router
from services.rag_service import get_rag_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan handler for startup and shutdown events."""
    # Startup
    logger.info("Starting LangChain RAG Assistant...")
    settings = get_settings()
    
    if not settings.openai_api_key:
        logger.warning("OPENAI_API_KEY not set. API will fail without it.")
    else:
        # Initialize RAG service
        try:
            rag_service = get_rag_service()
            await rag_service.initialize()
            logger.info("RAG service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize RAG service: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down LangChain RAG Assistant...")


# Create FastAPI app
app = FastAPI(
    title="LangChain RAG Assistant",
    description="A RAG-powered assistant for LangChain, LangGraph, and LangSmith documentation",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "LangChain RAG Assistant API",
        "version": "1.0.0",
        "description": "Ask questions about LangChain, LangGraph, and LangSmith",
        "docs_url": "/docs",
        "endpoints": {
            "chat": "POST /api/chat",
            "health": "GET /api/health",
            "index": "POST /api/index",
            "sources": "GET /api/sources"
        }
    }


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )
