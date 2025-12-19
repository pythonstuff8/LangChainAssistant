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
        *   `OPENAI_API_KEY`: Your OpenAI API key (sk-...).

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
