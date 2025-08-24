import * as React from 'react';

// API Types
export interface GenerateRequest {
  prompt: string;
  quality?: string;
}

export interface GenerateResponse {
  video_url: string;
  code: string;
  scene_name: string;
  status: string;
  description?: string;
  job_id?: string;
  progress?: number;
  current_step?: string;
  method?: string; // 'openai_generated' | 'sample_fallback' | 'emergency_fallback'
  model?: string;
  sample_used?: string;
}

export interface ExampleItem {
  title: string;
  prompt: string;
  video_url: string;
  thumbnail_url?: string;
  description: string;
  category: string;
  duration: string;
}

export interface ExampleResponse {
  examples: ExampleItem[];
}

export interface HealthResponse {
  status: string;
  message: string;
}

export interface APIError {
  error: string;
  message: string;
  details?: string;
}

export interface JobStatusResponse {
  job_id: string;
  status: string;
  progress: number;
  current_step: string;
  estimated_time_remaining?: number;
  video_url?: string;
  code?: string;
  scene_name?: string;
  error?: string;
  method?: string; // 'openai_generated' | 'sample_fallback' | 'emergency_fallback'
  model?: string;
  sample_used?: string;
}

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

class APIError extends Error {
  constructor(
    message: string, 
    public statusCode: number, 
    public details?: string
  ) {
    super(message);
    this.name = 'APIError';
  }
}

// HTTP Client
class APIClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private async request<T>(
    endpoint: string, 
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new APIError(
          errorData.message || `HTTP ${response.status}: ${response.statusText}`,
          response.status,
          errorData.details
        );
      }

      return await response.json();
    } catch (error) {
      if (error instanceof APIError) {
        throw error;
      }
      
      // Network or parsing errors
      throw new APIError(
        `Network error: ${error instanceof Error ? error.message : 'Unknown error'}`,
        0
      );
    }
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  async post<T>(endpoint: string, data: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }
}

// API Instance
const apiClient = new APIClient(API_BASE_URL);

// API Functions
export const api = {
  // Health check
  async health(): Promise<HealthResponse> {
    return apiClient.get<HealthResponse>('/api/health');
  },

  // Generate animation
  async generate(request: GenerateRequest): Promise<GenerateResponse> {
    return apiClient.post<GenerateResponse>('/api/generate', request);
  },

  // Get examples
  async getExamples(): Promise<ExampleResponse> {
    return apiClient.get<ExampleResponse>('/api/examples');
  },

  // Render animation (for direct rendering)
  async render(request: GenerateRequest): Promise<GenerateResponse> {
    return apiClient.post<GenerateResponse>('/api/render', request);
  },

  // Get job status
  async getJobStatus(jobId: string): Promise<JobStatusResponse> {
    return apiClient.get<JobStatusResponse>(`/api/job/${jobId}/status`);
  },

  // Clean up completed job
  async cleanupJob(jobId: string): Promise<{ message: string }> {
    return apiClient.delete<{ message: string }>(`/api/job/${jobId}`);
  }
};

// Utility function for building full URLs
export function buildMediaUrl(path: string): string {
  if (path.startsWith('http')) {
    return path;
  }
  return `${API_BASE_URL}${path}`;
}

// Hook for API status
export function useAPIStatus() {
  const [isOnline, setIsOnline] = React.useState<boolean>(true);
  const [lastChecked, setLastChecked] = React.useState<Date>(new Date());

  React.useEffect(() => {
    const checkStatus = async () => {
      try {
        await api.health();
        setIsOnline(true);
      } catch {
        setIsOnline(false);
      }
      setLastChecked(new Date());
    };

    checkStatus();
    const interval = setInterval(checkStatus, 30000); // Check every 30 seconds

    return () => clearInterval(interval);
  }, []);

  return { isOnline, lastChecked };
}

export { APIError };