"""Chat API routes for the RAG assistant."""

import logging
from typing import Optional, List
from fastapi import APIRouter, HTTPException

from models.schemas import (
    ChatRequest, 
    ChatResponse, 
    HealthResponse, 
    IndexResponse,
    ServiceFilter
)
from services.rag_service import get_rag_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Check the health of the API and vector store status.
    """
    rag_service = get_rag_service()
    return HealthResponse(
        status="healthy",
        vector_store_ready=rag_service.is_initialized,
        indexed_documents=rag_service.document_count
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Submit a question and get an AI-generated answer with source citations.
    
    The answer is generated using RAG (Retrieval-Augmented Generation) from
    the LangChain, LangGraph, and LangSmith documentation.
    """
    try:
        rag_service = get_rag_service()
        
        answer, sources, processing_time = await rag_service.query(
            question=request.question,
            service_filter=request.service_filter
        )
        
        return ChatResponse(
            answer=answer,
            sources=sources,
            processing_time=round(processing_time, 2)
        )
    
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process question: {str(e)}"
        )


@router.post("/index", response_model=IndexResponse)
async def index_documents(services: Optional[List[str]] = None):
    """
    Trigger re-indexing of documentation.
    
    Optionally specify which services to re-index:
    - langchain
    - langgraph
    - langsmith
    
    If no services specified, all documentation will be re-indexed.
    """
    try:
        rag_service = get_rag_service()
        
        docs_count, indexed_services = await rag_service.index_documents(services)
        
        return IndexResponse(
            success=True,
            documents_indexed=docs_count,
            services_indexed=indexed_services,
            message=f"Successfully indexed {docs_count} document chunks"
        )
    
    except Exception as e:
        logger.error(f"Error indexing documents: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to index documents: {str(e)}"
        )


@router.get("/sources")
async def list_sources():
    """
    List the available documentation sources.
    """
    return {
        "sources": [
            {
                "name": "LangChain",
                "id": "langchain",
                "description": "Core LangChain framework for building LLM applications",
                "docs_url": "https://python.langchain.com/docs"
            },
            {
                "name": "LangGraph",
                "id": "langgraph",
                "description": "Library for building stateful, multi-actor LLM applications",
                "docs_url": "https://langchain-ai.github.io/langgraph"
            },
            {
                "name": "LangSmith",
                "id": "langsmith",
                "description": "Platform for debugging, testing, and monitoring LLM applications",
                "docs_url": "https://docs.smith.langchain.com"
            }
        ]
    }
