"""RAG Service for handling question-answering with document retrieval."""

import logging
import time
from typing import List, Optional, Tuple
from pathlib import Path

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
from langchain.schema.runnable import RunnablePassthrough

from config import get_settings
from models.schemas import Source, ServiceFilter
from services.doc_loader import DocumentLoader, get_sample_documents

logger = logging.getLogger(__name__)


class RAGService:
    """Service for Retrieval-Augmented Generation using LangChain documentation."""
    
    def __init__(self):
        """Initialize the RAG service."""
        self.settings = get_settings()
        self._vectorstore: Optional[Chroma] = None
        self._embeddings: Optional[OpenAIEmbeddings] = None
        self._llm: Optional[ChatOpenAI] = None
        self._initialized = False
        self._document_count = 0
    
    @property
    def is_initialized(self) -> bool:
        """Check if the RAG service is initialized."""
        return self._initialized
    
    @property
    def document_count(self) -> int:
        """Get the number of documents in the vector store."""
        return self._document_count
    
    def _get_embeddings(self) -> OpenAIEmbeddings:
        """Get or create embeddings model."""
        if self._embeddings is None:
            self._embeddings = OpenAIEmbeddings(
                model=self.settings.openai_embedding_model,
                openai_api_key=self.settings.openai_api_key
            )
        return self._embeddings
    
    def _get_llm(self) -> ChatOpenAI:
        """Get or create LLM."""
        if self._llm is None:
            self._llm = ChatOpenAI(
                model=self.settings.openai_chat_model,
                openai_api_key=self.settings.openai_api_key,
                temperature=0.1
            )
        return self._llm
    
    def _get_vectorstore(self) -> Chroma:
        """Get or create vector store."""
        if self._vectorstore is None:
            persist_dir = Path(self.settings.chroma_persist_directory)
            persist_dir.mkdir(parents=True, exist_ok=True)
            
            self._vectorstore = Chroma(
                collection_name=self.settings.collection_name,
                embedding_function=self._get_embeddings(),
                persist_directory=str(persist_dir)
            )
        return self._vectorstore
    
    async def initialize(self, force_reindex: bool = False) -> int:
        """
        Initialize the RAG service and load documents if needed.
        
        Args:
            force_reindex: If True, reload all documents even if vector store exists.
            
        Returns:
            Number of documents indexed.
        """
        logger.info("Initializing RAG service...")
        
        vectorstore = self._get_vectorstore()
        
        # Check if we already have documents
        try:
            collection = vectorstore._collection
            existing_count = collection.count()
            logger.info(f"Found {existing_count} existing documents in vector store")
        except Exception:
            existing_count = 0
        
        if existing_count > 0 and not force_reindex:
            self._document_count = existing_count
            self._initialized = True
            logger.info("Using existing vector store")
            return existing_count
        
        # Load and index documents
        logger.info("Loading documentation...")
        doc_loader = DocumentLoader()
        
        try:
            # Try to load from web
            documents = doc_loader.load_and_split()
        except Exception as e:
            logger.warning(f"Web loading failed: {e}. Using sample documents.")
            documents = get_sample_documents()
            # Split sample documents
            documents = doc_loader.split_documents(documents)
        
        if not documents:
            logger.warning("No documents loaded. Using sample documents.")
            documents = get_sample_documents()
            documents = doc_loader.split_documents(documents)
        
        # Add to vector store
        logger.info(f"Indexing {len(documents)} document chunks...")
        
        if force_reindex:
            # Clear existing collection
            try:
                vectorstore._collection.delete(where={})
            except Exception:
                pass
        
        vectorstore.add_documents(documents)
        self._document_count = len(documents)
        self._initialized = True
        
        logger.info(f"RAG service initialized with {self._document_count} chunks")
        return self._document_count
    
    async def index_documents(self, services: Optional[List[str]] = None) -> Tuple[int, List[str]]:
        """
        Re-index documentation for specified services.
        
        Args:
            services: List of services to index. If None, indexes all.
            
        Returns:
            Tuple of (document count, list of indexed services).
        """
        if services is None:
            services = ["langchain", "langgraph", "langsmith"]
        
        doc_loader = DocumentLoader()
        
        try:
            documents = doc_loader.load_and_split(services)
        except Exception as e:
            logger.warning(f"Web loading failed: {e}. Using sample documents.")
            documents = get_sample_documents(services)
            documents = doc_loader.split_documents(documents)
        
        vectorstore = self._get_vectorstore()
        
        # Remove existing documents for these services
        for service in services:
            try:
                vectorstore._collection.delete(where={"service": service})
            except Exception:
                pass
        
        # Add new documents
        vectorstore.add_documents(documents)
        self._document_count = vectorstore._collection.count()
        
        return len(documents), services
    
    def _format_docs(self, docs: List[Document]) -> str:
        """Format documents for context."""
        return "\n\n---\n\n".join(
            f"Source: {doc.metadata.get('title', 'Unknown')}\n{doc.page_content}"
            for doc in docs
        )
    
    def _create_sources(self, docs: List[Document]) -> List[Source]:
        """Create Source objects from retrieved documents."""
        sources = []
        seen_urls = set()
        
        for doc in docs:
            url = doc.metadata.get("source", "")
            if url in seen_urls:
                continue
            seen_urls.add(url)
            
            sources.append(Source(
                title=doc.metadata.get("title", "Documentation"),
                url=url,
                content_preview=doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                service=doc.metadata.get("service", "langchain")
            ))
        
        return sources[:5]  # Limit to 5 sources
    
    async def query(
        self,
        question: str,
        service_filter: ServiceFilter = ServiceFilter.ALL
    ) -> Tuple[str, List[Source], float]:
        """
        Query the RAG system with a question.
        
        Args:
            question: The user's question.
            service_filter: Filter to specific service documentation.
            
        Returns:
            Tuple of (answer, sources, processing_time).
        """
        start_time = time.time()
        
        if not self._initialized:
            await self.initialize()
        
        vectorstore = self._get_vectorstore()
        llm = self._get_llm()
        
        # Build retriever with optional filter
        search_kwargs = {"k": 5}
        if service_filter != ServiceFilter.ALL:
            search_kwargs["filter"] = {"service": service_filter.value}
        
        retriever = vectorstore.as_retriever(search_kwargs=search_kwargs)
        
        # Retrieve relevant documents
        docs = retriever.invoke(question)
        
        if not docs:
            processing_time = time.time() - start_time
            return (
                "I couldn't find relevant information in the documentation. Please try rephrasing your question or check the official documentation directly.",
                [],
                processing_time
            )
        
        # Create prompt
        prompt = ChatPromptTemplate.from_template("""You are a helpful assistant specializing in LangChain, LangGraph, and LangSmith documentation. 
Answer the user's question based on the provided context. Be concise but thorough. 
If the context doesn't contain enough information, say so and provide what you can.
Include code examples when relevant.

Context:
{context}

Question: {question}

Answer:""")
        
        # Create and run chain
        chain = (
            {"context": lambda x: self._format_docs(docs), "question": RunnablePassthrough()}
            | prompt
            | llm
        )
        
        response = chain.invoke(question)
        answer = response.content
        
        # Create sources
        sources = self._create_sources(docs)
        
        processing_time = time.time() - start_time
        
        return answer, sources, processing_time


# Global instance
_rag_service: Optional[RAGService] = None


def get_rag_service() -> RAGService:
    """Get or create the global RAG service instance."""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service
