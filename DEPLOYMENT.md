# Deployment Guide

This guide describes how to deploy the combined LangChain Assistant (Frontend + Backend) to Vercel.

## Deployment Steps

1.  **Push to GitHub**
    *   Ensure your code is pushed to a GitHub repository.

2.  **Import to Vercel**
    *   Go to [Vercel](https://vercel.com) and click "Add New... Project".
    *   Select your GitHub repository.

3.  **Configure Project**
    *   **Framework Preset**: Next.js (should detect automatically).
    *   **Root Directory**: Leave as `./` (default).
    *   Vercel will automatically detect the Python backend in `api/` and the Next.js frontend.

4.  **Environment Variables**
    *   Add the following environment variables in the Vercel dashboard:
        *   `OPENAI_API_KEY`: **(Required)** Your OpenAI API key (starts with `sk-`).
        *   `OPENAI_CHAT_MODEL`: *Optional* (defaults to `gpt-4o-mini`).
        *   `OPENAI_EMBEDDING_MODEL`: *Optional* (defaults to `text-embedding-3-small`).
        *   `CHROMA_PERSIST_DIRECTORY`: *Optional* (defaults to `./data/chroma_db`).
        *   `NEXT_PUBLIC_API_URL`: *Optional* (defaults to your Vercel deployment URL). Only set this if you want to point to a different backend.

5.  **Deploy**
    *   Click "Deploy".
    *   Vercel will build the frontend and set up the serverless functions for the backend.

## Local Development

To run the project locally with the new structure:

1.  **Install Dependencies**:
    ```bash
    npm install
    pip install -r requirements.txt
    ```

2.  **Run Backend** (in one terminal):
    ```bash
    python -m uvicorn backend.main:app --reload --port 8000
    ```

3.  **Run Frontend** (in another terminal):
    ```bash
    npm run dev
    ```
    *   The frontend is configured to proxy `/api/*` requests to `http://127.0.0.1:8000/api/*`.
