import axios from 'axios';

const API_URL = '/v1';

export const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
        // Using local dev key as configured in docker-compose
        'X-API-Key': 'local-dev-api-key'
    },
    withCredentials: true // Send cookies with requests
});

// Cookies are automatically sent by browser, no need for interceptor

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

// ============================================
// Brain API Functions
// ============================================

export interface BrainRecallResponse {
    query: string;
    result: string;
    matches?: Array<{
        fact_id: string;
        content: string;
        created_at: string;
        relevance: string;
    }>;
    suggestion?: string;
    metadata?: {
        facts_retrieved: number;
        level_used: number;
        confidence: number;
        compression_ratio: number;
        user_query_count: number;
        user_fact_count: number;
    };
}

export interface BrainInsight {
    summary: string;
    patterns: string[];
    sentiment: string;
    consolidated_memories?: number;
    key_insights?: string[];
}

export interface BrainStatusResponse {
    status: string;
    logicalBrain: string;
    intuitiveBrain: string;
}

/**
 * Query the logical brain for fact recall
 * @param query - Search query string
 */
export const recallFromBrain = async (query: string): Promise<BrainRecallResponse> => {
    const response = await api.post<BrainRecallResponse>('/logical/recall', null, {
        params: { query }
    });
    return response.data;
};

/**
 * Trigger the intuitive brain's dream cycle for pattern detection
 * @param facts - Array of facts to consolidate
 */
export const triggerDreamCycle = async (facts: Array<{ content: string; fact_id: string; created_at: string }>): Promise<BrainInsight> => {
    const response = await api.post<BrainInsight>('/intuitive/dream', {
        user_id: "default", // TODO: Get actual user ID
        facts: facts.map(f => f.content)
    });
    return response.data;
};

/**
 * Get the current brain integration status
 */
export const getBrainStatus = async (): Promise<BrainStatusResponse> => {
    const response = await api.get<any>('/stats');
    return {
        status: response.data.status || "operational",
        logicalBrain: response.data.llama_available ? "online" : "offline",
        intuitiveBrain: "online"
    };
};
