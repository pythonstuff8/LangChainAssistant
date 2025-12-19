# LangChain RAG Documentation Assistant

A full-stack RAG (Retrieval-Augmented Generation) assistant that helps users with LangChain, LangGraph, and LangSmith documentation.

![LangChain Assistant](https://img.shields.io/badge/LangChain-Assistant-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![Next.js](https://img.shields.io/badge/Next.js-14-black)

## Features

- 🤖 **AI-Powered Q&A** - Ask questions about LangChain, LangGraph, and LangSmith
- 📚 **Documentation RAG** - Retrieves relevant documentation snippets for accurate answers
- 🎯 **Service Filtering** - Filter answers to specific services
- 📖 **Source Citations** - See exactly which documentation was used
- 🌙 **Modern Dark UI** - Beautiful glassmorphism design with animations

## Project Structure

```
LangChainAssist/
├── backend/                 # FastAPI backend
│   ├── main.py             # Application entry point
│   ├── config.py           # Configuration settings
│   ├── requirements.txt    # Python dependencies
│   ├── routers/            # API routes
│   ├── services/           # Business logic (RAG, doc loading)
│   └── models/             # Pydantic schemas
│
└── frontend/               # Next.js frontend
    ├── src/
    │   ├── app/            # Next.js app router
    │   ├── components/     # React components
    │   └── lib/            # API client
    └── package.json
```

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- OpenAI API key

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Start the server
python main.py
```

The API will be available at http://localhost:8000

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at http://localhost:3000


### 3. Docker Setup (Recommended)

The easiest way to run the application is using Docker Compose.

1. Ensure you have Docker and Docker Compose installed.
2. Create the environment files:
   ```bash
   # Backend
   cp backend/.env.example backend/.env
   # Edit backend/.env and add your OPENAI_API_KEY
   
   # Frontend
   cp frontend/.env.local.example frontend/.env.local
   ```
3. Run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

The application will be available at:
- Frontend: http://localhost:3006
- Backend docs: http://localhost:3005/docs

### 4. Running Locally (No Docker)

If you prefer to run it manually ("regularly") on your computer:

**Terminal 1: Backend**
```bash
cd backend
# Install python dependencies
pip install -r requirements.txt
# Run the server
python main.py
```

**Terminal 2: Frontend**
```bash
cd frontend
# Install node dependencies
npm install
# Run the development server
npm run dev
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/chat` | POST | Submit a question, get AI answer with sources |
| `/api/health` | GET | Health check and vector store status |
| `/api/sources` | GET | List available documentation sources |
| `/api/index` | POST | Trigger re-indexing of documentation |

### Example Request

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I create a chain in LangChain?", "service_filter": "langchain"}'
```

## Configuration

### Environment Variables (Backend)

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `OPENAI_CHAT_MODEL` | Chat model to use | `gpt-4o-mini` |
| `OPENAI_EMBEDDING_MODEL` | Embedding model | `text-embedding-3-small` |
| `CHUNK_SIZE` | Document chunk size | `1000` |
| `CHUNK_OVERLAP` | Chunk overlap | `200` |

### Environment Variables (Frontend)

Create a `.env.local` file:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Technologies

- **Backend**: FastAPI, LangChain, ChromaDB, OpenAI
- **Frontend**: Next.js 14, React, Tailwind CSS, TypeScript
- **RAG Pipeline**: Document loading, chunking, embedding, vector search

## Infrastructure Requirements

Since this application uses OpenAI for LLM and Embeddings, the local resource requirements are lightweight.

**Recommended Configuration:**
- **CPU**: 2 vCPUs (sufficient for web server and vector search)
- **RAM**: 4GB (Next.js build/runtime + FastAPI + ChromaDB)
- **GPU**: **None Required** (All heavy AI lifting is done via OpenAI API)
- **Storage**: 10GB+ SSD (for Docker images and vector database)

**Why no GPU?**
The generic "GPU" requirement for AI apps usually applies when running local LLMs (like Llama 2, Mistral). This app is "Cloud Native AI" - it sends text to OpenAI and gets answers back. Your server just acts as a coordinator.

## License

MIT
# LangChainAssistant-Frontend
