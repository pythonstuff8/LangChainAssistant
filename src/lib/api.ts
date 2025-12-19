/**
 * API client for communicating with the FastAPI backend.
 */

import axios, { AxiosError } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3005';

export type ServiceFilter = 'all' | 'langchain' | 'langgraph' | 'langsmith';

export interface Source {
    title: string;
    url: string;
    content_preview: string;
    service: string;
}

export interface ChatRequest {
    question: string;
    service_filter?: ServiceFilter;
}

export interface ChatResponse {
    answer: string;
    sources: Source[];
    processing_time: number;
}

export interface HealthResponse {
    status: string;
    vector_store_ready: boolean;
    indexed_documents: number;
}

export interface ServiceInfo {
    name: string;
    id: string;
    description: string;
    docs_url: string;
}

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 60000, // 60 second timeout for RAG queries
});

/**
 * Send a chat message and get an AI-generated response.
 */
export async function sendChatMessage(
    question: string,
    serviceFilter: ServiceFilter = 'all'
): Promise<ChatResponse> {
    try {
        const response = await api.post<ChatResponse>('/api/chat', {
            question,
            service_filter: serviceFilter,
        });
        return response.data;
    } catch (error) {
        if (error instanceof AxiosError) {
            throw new Error(error.response?.data?.detail || 'Failed to get response');
        }
        throw error;
    }
}

/**
 * Check the health status of the API.
 */
export async function checkHealth(): Promise<HealthResponse> {
    try {
        const response = await api.get<HealthResponse>('/api/health');
        return response.data;
    } catch (error) {
        if (error instanceof AxiosError) {
            throw new Error('API is unavailable');
        }
        throw error;
    }
}

/**
 * Get list of available documentation sources.
 */
export async function getSources(): Promise<ServiceInfo[]> {
    try {
        const response = await api.get<{ sources: ServiceInfo[] }>('/api/sources');
        return response.data.sources;
    } catch (error) {
        if (error instanceof AxiosError) {
            throw new Error('Failed to fetch sources');
        }
        throw error;
    }
}

/**
 * Trigger re-indexing of documentation.
 */
export async function reindexDocuments(services?: string[]): Promise<void> {
    try {
        await api.post('/api/index', null, {
            params: services ? { services: services.join(',') } : undefined,
        });
    } catch (error) {
        if (error instanceof AxiosError) {
            throw new Error(error.response?.data?.detail || 'Failed to reindex');
        }
        throw error;
    }
}

export default api;
