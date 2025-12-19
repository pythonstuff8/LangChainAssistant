# Deployment Guide

Due to Vercel's 250MB size limit for Python functions, it is recommended to deploy the **Frontend on Vercel** and the **Backend on Render**.

## 1. Backend (FastAPI) -> Deploy to Render

Render has no strict size limits, making it perfect for Python RAG apps.

1.  **Push to GitHub**: Ensure your code is in a GitHub repository.
2.  **Create Web Service**:
    *   Go to [Render Dashboard](https://dashboard.render.com).
    *   Click "New +" -> "Web Service".
    *   Select your GitHub repository.
3.  **Configure**:
    *   **Name**: `langchain-assistant-api`
    *   **Root Directory**: `backend`
    *   **Runtime**: `Python 3`
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4.  **Environment Variables**:
    *   Click "Advanced" -> "Add Environment Variable".
    *   `OPENAI_API_KEY`: `your_key_here`
5.  **Deploy**: Click "Create Web Service".
6.  **Copy URL**: Once deployed, copy your backend URL (e.g., `https://langchain-assistant-api.onrender.com`).

---

## 2. Frontend (Next.js) -> Deploy to Vercel

1.  **Import to Vercel**:
    *   Go to [Vercel](https://vercel.com) and click "Add New... Project".
    *   Select the same GitHub repository.
2.  **Configure**:
    *   **Framework Preset**: Next.js
    *   **Root Directory**: `./` (default)
3.  **Environment Variables**:
    *   `NEXT_PUBLIC_API_URL`: **Paste your Render URL here** (e.g., `https://langchain-assistant-api.onrender.com`).
4.  **Deploy**: Click "Deploy".

---

## Local Development

1.  **Install Dependencies**:
    ```bash
    npm install
    pip install -r requirements.txt
    ```

2.  **Run Backend**:
    ```bash
    python -m uvicorn backend.main:app --reload --port 8000
    ```

3.  **Run Frontend**:
    ```bash
    npm run dev
    ```
