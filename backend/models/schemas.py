"""Pydantic models for API request and response schemas."""

from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class ServiceFilter(str, Enum):
    """Available documentation services to filter by."""
    ALL = "all"
    LANGCHAIN = "langchain"
    LANGGRAPH = "langgraph"
    LANGSMITH = "langsmith"


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    question: str = Field(..., min_length=1, max_length=2000, description="The user's question")
    service_filter: ServiceFilter = Field(
        default=ServiceFilter.ALL,
        description="Filter to search specific service documentation"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "How do I create a simple chain in LangChain?",
                "service_filter": "langchain"
            }
        }


class Source(BaseModel):
    """Model for a documentation source reference."""
    title: str = Field(..., description="Title of the source document")
    url: str = Field(..., description="URL to the source document")
    content_preview: str = Field(..., description="Preview snippet of the source content")
    service: str = Field(..., description="Which service this source belongs to")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    answer: str = Field(..., description="The AI-generated answer")
    sources: List[Source] = Field(default=[], description="Source documents used to generate the answer")
    processing_time: float = Field(..., description="Time taken to process the request in seconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "To create a simple chain in LangChain, you can use the LCEL (LangChain Expression Language)...",
                "sources": [
                    {
                        "title": "LCEL Quickstart",
                        "url": "https://python.langchain.com/docs/expression_language/get_started",
                        "content_preview": "LCEL makes it easy to build complex chains...",
                        "service": "langchain"
                    }
                ],
                "processing_time": 1.23
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str = Field(..., description="Service health status")
    vector_store_ready: bool = Field(..., description="Whether the vector store is initialized")
    indexed_documents: int = Field(..., description="Number of documents in the vector store")


class IndexResponse(BaseModel):
    """Response model for index endpoint."""
    success: bool = Field(..., description="Whether indexing was successful")
    documents_indexed: int = Field(..., description="Number of documents indexed")
    services_indexed: List[str] = Field(..., description="List of services that were indexed")
    message: str = Field(..., description="Status message")
