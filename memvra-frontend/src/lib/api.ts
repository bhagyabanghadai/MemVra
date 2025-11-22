import axios from 'axios';

const API_URL = '/v1';

export const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
        // Using local dev key as configured in docker-compose
        'X-API-Key': 'local-dev-api-key'
    },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export interface FactRecord {
    fact_id: string;
    content: string;
    source_type: string;
    source_id: string;
    recorded_by: string;
    created_at: string;
    signature: string;
    revoked: boolean;
    revocation_reason?: string;
    revoked_at?: string;
}

export interface Page<T> {
    content: T[];
    totalPages: number;
    totalElements: number;
    size: number;
    number: number;
}

export interface ApiKey {
    keyId: string;
    name: string;
    createdAt: string;
    revoked: boolean;
    lastUsedAt?: string;
}

export const searchFacts = async (params: { source_id?: string; recorded_by?: string; source_type?: string; from_date?: string; to_date?: string; page?: number; size?: number }) => {
    const response = await api.get<Page<FactRecord>>('/facts', { params });
    return response.data;
};

export const getFact = async (id: string) => {
    const response = await api.get<FactRecord>(`/facts/${id}`);
    return response.data;
};

export const recordFact = async (data: { content: string; source_type: string; source_id: string; recorded_by: string }) => {
    const response = await api.post<FactRecord>('/facts', data);
    return response.data;
};

export const revokeFact = async (id: string, reason: string) => {
    await api.post(`/facts/${id}/revoke`, { reason });
};

export const login = async (credentials: any) => {
    const response = await api.post('/auth/login', credentials);
    return response.data;
};

export const signup = async (data: any) => {
    const response = await api.post('/auth/signup', data);
    return response.data;
};

export const getApiKeys = async () => {
    const response = await api.get<ApiKey[]>('/dashboard/keys');
    return response.data;
};

export const createApiKey = async (name: string) => {
    const response = await api.post<{ key: string }>('/dashboard/keys', { name });
    return response.data;
};

export const revokeApiKey = async (id: string) => {
    await api.delete(`/dashboard/keys/${id}`);
};
