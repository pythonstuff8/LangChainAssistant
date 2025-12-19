"""Document loader service for fetching and processing LangChain documentation."""

import logging
from typing import List, Dict, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import requests
from bs4 import BeautifulSoup
import html2text
import re

from config import get_settings

logger = logging.getLogger(__name__)


class DocumentLoader:
    """Service for loading and processing documentation from LangChain ecosystem."""
    
    # Key documentation pages for each service
    LANGCHAIN_PAGES = [
        ("https://python.langchain.com/docs/get_started/introduction", "LangChain Introduction"),
        ("https://python.langchain.com/docs/get_started/quickstart", "LangChain Quickstart"),
        ("https://python.langchain.com/docs/modules/model_io/", "Model I/O"),
        ("https://python.langchain.com/docs/modules/chains/", "Chains"),
        ("https://python.langchain.com/docs/modules/agents/", "Agents"),
        ("https://python.langchain.com/docs/modules/memory/", "Memory"),
        ("https://python.langchain.com/docs/expression_language/", "LCEL"),
        ("https://python.langchain.com/docs/expression_language/get_started", "LCEL Quickstart"),
        ("https://python.langchain.com/docs/modules/data_connection/", "Data Connection"),
        ("https://python.langchain.com/docs/integrations/llms/openai", "OpenAI Integration"),
        ("https://python.langchain.com/docs/integrations/chat/openai", "OpenAI Chat"),
        ("https://python.langchain.com/docs/integrations/vectorstores/chroma", "Chroma Integration"),
    ]
    
    LANGGRAPH_PAGES = [
        ("https://langchain-ai.github.io/langgraph/", "LangGraph Introduction"),
        ("https://langchain-ai.github.io/langgraph/tutorials/introduction/", "LangGraph Tutorial"),
        ("https://langchain-ai.github.io/langgraph/concepts/", "LangGraph Concepts"),
        ("https://langchain-ai.github.io/langgraph/how-tos/", "LangGraph How-To Guides"),
        ("https://langchain-ai.github.io/langgraph/concepts/low_level/", "Low Level Concepts"),
        ("https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/", "Agentic Concepts"),
    ]
    
    LANGSMITH_PAGES = [
        ("https://docs.smith.langchain.com/", "LangSmith Introduction"),
        ("https://docs.smith.langchain.com/tracing", "LangSmith Tracing"),
        ("https://docs.smith.langchain.com/evaluation", "LangSmith Evaluation"),
        ("https://docs.smith.langchain.com/prompts", "LangSmith Prompts"),
        ("https://docs.smith.langchain.com/observability", "LangSmith Observability"),
    ]
    
    def __init__(self):
        """Initialize the document loader."""
        self.settings = get_settings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.settings.chunk_size,
            chunk_overlap=self.settings.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = True
        self.html_converter.body_width = 0
    
    def _fetch_page(self, url: str) -> Optional[str]:
        """Fetch a web page and return its HTML content."""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; LangChainRAGBot/1.0)"
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.warning(f"Failed to fetch {url}: {e}")
            return None
    
    def _extract_content(self, html: str, url: str) -> str:
        """Extract main content from HTML page."""
        soup = BeautifulSoup(html, "html.parser")
        
        # Remove script, style, nav, and footer elements
        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.decompose()
        
        # Try to find main content area
        main_content = (
            soup.find("main") or 
            soup.find("article") or 
            soup.find(class_=re.compile(r"content|main|article|doc", re.I)) or
            soup.find("div", class_=re.compile(r"markdown|prose", re.I)) or
            soup.body
        )
        
        if main_content:
            # Convert to markdown
            markdown = self.html_converter.handle(str(main_content))
            # Clean up excessive whitespace
            markdown = re.sub(r'\n{3,}', '\n\n', markdown)
            return markdown.strip()
        
        return ""
    
    def _determine_service(self, url: str) -> str:
        """Determine which service a URL belongs to."""
        if "langgraph" in url.lower():
            return "langgraph"
        elif "smith" in url.lower():
            return "langsmith"
        else:
            return "langchain"
    
    def load_documents(self, services: Optional[List[str]] = None) -> List[Document]:
        """
        Load documentation for specified services.
        
        Args:
            services: List of services to load. If None, loads all services.
            
        Returns:
            List of Document objects with content and metadata.
        """
        if services is None:
            services = ["langchain", "langgraph", "langsmith"]
        
        all_documents = []
        pages_to_load = []
        
        if "langchain" in services:
            pages_to_load.extend([(url, title, "langchain") for url, title in self.LANGCHAIN_PAGES])
        if "langgraph" in services:
            pages_to_load.extend([(url, title, "langgraph") for url, title in self.LANGGRAPH_PAGES])
        if "langsmith" in services:
            pages_to_load.extend([(url, title, "langsmith") for url, title in self.LANGSMITH_PAGES])
        
        for url, title, service in pages_to_load:
            logger.info(f"Loading: {title} ({url})")
            html = self._fetch_page(url)
            
            if html:
                content = self._extract_content(html, url)
                if content:
                    # Create a document with metadata
                    doc = Document(
                        page_content=content,
                        metadata={
                            "source": url,
                            "title": title,
                            "service": service
                        }
                    )
                    all_documents.append(doc)
                    logger.info(f"  Loaded {len(content)} characters")
        
        logger.info(f"Loaded {len(all_documents)} documents total")
        return all_documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into smaller chunks for embedding.
        
        Args:
            documents: List of full documents to split.
            
        Returns:
            List of chunked Document objects.
        """
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Split {len(documents)} documents into {len(chunks)} chunks")
        return chunks
    
    def load_and_split(self, services: Optional[List[str]] = None) -> List[Document]:
        """
        Load and split documentation in one step.
        
        Args:
            services: List of services to load.
            
        Returns:
            List of chunked Document objects.
        """
        documents = self.load_documents(services)
        return self.split_documents(documents)


# Fallback sample documentation if web scraping fails
SAMPLE_DOCS = {
    "langchain": [
        Document(
            page_content="""# LangChain Introduction

LangChain is a framework for developing applications powered by large language models (LLMs).

## Key Concepts

### Chains
Chains are sequences of calls - whether to an LLM, a tool, or a data preprocessing step. LangChain provides a standard interface for chains, allowing you to create sequences of calls and integrate them with other tools.

```python
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini")
prompt = PromptTemplate.from_template("Tell me about {topic}")
chain = LLMChain(llm=llm, prompt=prompt)
result = chain.invoke({"topic": "LangChain"})
```

### LCEL (LangChain Expression Language)
LCEL is a declarative way to compose chains. It supports streaming, async, and batch operations out of the box.

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("Tell me about {topic}")
model = ChatOpenAI()
chain = prompt | model
response = chain.invoke({"topic": "AI"})
```

### Agents
Agents use LLMs to determine which actions to take and in what order. An agent has access to a suite of tools, and it decides which tool to use based on user input.

```python
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.tools import tool

@tool
def search(query: str) -> str:
    \"\"\"Search for information.\"\"\"
    return f"Results for: {query}"

llm = ChatOpenAI(model="gpt-4o-mini")
tools = [search]
agent = create_openai_functions_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)
```

### Memory
Memory allows a chain or agent to remember previous interactions with the user.

```python
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory()
memory.save_context({"input": "hi"}, {"output": "hello"})
```""",
            metadata={"source": "https://python.langchain.com/docs", "title": "LangChain Introduction", "service": "langchain"}
        ),
        Document(
            page_content="""# RAG with LangChain

Retrieval-Augmented Generation (RAG) is a technique that combines retrieval of relevant documents with LLM generation.

## Building a RAG Pipeline

### 1. Load Documents
```python
from langchain.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://example.com/docs")
docs = loader.load()
```

### 2. Split Documents
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)
```

### 3. Create Embeddings and Store
```python
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings)
```

### 4. Create Retrieval Chain
```python
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)
result = qa_chain.invoke("What is this about?")
```""",
            metadata={"source": "https://python.langchain.com/docs/use_cases/rag", "title": "RAG with LangChain", "service": "langchain"}
        ),
    ],
    "langgraph": [
        Document(
            page_content="""# LangGraph Introduction

LangGraph is a library for building stateful, multi-actor applications with LLMs. It extends LangChain to enable cyclic computational graphs.

## Key Concepts

### StateGraph
A StateGraph is the main abstraction in LangGraph. It defines a graph of nodes and edges.

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class State(TypedDict):
    messages: list
    next_step: str

graph = StateGraph(State)
```

### Nodes
Nodes are functions that take the current state and return updates to apply.

```python
def chatbot(state: State) -> dict:
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}

graph.add_node("chatbot", chatbot)
```

### Edges
Edges define the flow between nodes. They can be conditional or unconditional.

```python
# Unconditional edge
graph.add_edge("start", "chatbot")

# Conditional edge
def should_continue(state: State) -> str:
    if state["next_step"] == "end":
        return END
    return "chatbot"

graph.add_conditional_edges("chatbot", should_continue)
```

### Compiling and Running
```python
app = graph.compile()
result = app.invoke({"messages": ["Hello!"], "next_step": "continue"})
```

## Building Agents with LangGraph

LangGraph is ideal for building agents because it allows for:
- Cycles (agents can loop back to reconsider)
- State persistence
- Human-in-the-loop workflows
- Multi-agent orchestration""",
            metadata={"source": "https://langchain-ai.github.io/langgraph/", "title": "LangGraph Introduction", "service": "langgraph"}
        ),
    ],
    "langsmith": [
        Document(
            page_content="""# LangSmith Introduction

LangSmith is a platform for debugging, testing, evaluating, and monitoring LLM applications.

## Key Features

### Tracing
Automatically trace all LLM calls, chain executions, and agent steps.

```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"
os.environ["LANGCHAIN_PROJECT"] = "my-project"

# All LangChain operations are now traced automatically
from langchain_openai import ChatOpenAI
llm = ChatOpenAI()
response = llm.invoke("Hello!")  # This call is traced
```

### Evaluation
Create datasets and run evaluations on your LLM applications.

```python
from langsmith import Client
client = Client()

# Create a dataset
dataset = client.create_dataset("my-dataset")
client.create_example(
    inputs={"question": "What is LangChain?"},
    outputs={"answer": "A framework for LLM applications"},
    dataset_id=dataset.id
)

# Run evaluation
from langsmith.evaluation import evaluate
results = evaluate(
    my_chain,
    data="my-dataset",
    evaluators=["qa"]
)
```

### Prompt Management
Manage and version your prompts in LangSmith.

```python
from langchain import hub

# Pull a prompt from the hub
prompt = hub.pull("rlm/rag-prompt")

# Push a prompt
hub.push("my-org/my-prompt", prompt)
```

### Monitoring
Monitor your production LLM applications:
- Track latency, token usage, and costs
- Set up alerts for errors or anomalies
- View traces in real-time""",
            metadata={"source": "https://docs.smith.langchain.com/", "title": "LangSmith Introduction", "service": "langsmith"}
        ),
    ],
}


def get_sample_documents(services: Optional[List[str]] = None) -> List[Document]:
    """Get sample documents for when web scraping is unavailable."""
    if services is None:
        services = ["langchain", "langgraph", "langsmith"]
    
    docs = []
    for service in services:
        if service in SAMPLE_DOCS:
            docs.extend(SAMPLE_DOCS[service])
    
    return docs
