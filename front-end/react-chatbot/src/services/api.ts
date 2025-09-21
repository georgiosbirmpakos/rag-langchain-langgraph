// Modern API service layer using fetch with proper error handling
// This centralizes all API calls and provides a clean interface

import { API_BASE } from '../types';
import type { ChatResponse, SampleQuestionsResponse, ConversationHistory, StatsResponse } from '../types';

// Custom error class for API errors
export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public statusText: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

// Generic fetch wrapper with error handling
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  
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
      throw new ApiError(
        errorData.detail || `HTTP Error: ${response.status}`,
        response.status,
        response.statusText
      );
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    
    // Network or other errors
    throw new ApiError(
      `Network error: ${error instanceof Error ? error.message : 'Unknown error'}`,
      0,
      'Network Error'
    );
  }
}

// API service functions
export const apiService = {
  // Send a message to the chatbot
  async sendMessage(question: string): Promise<ChatResponse> {
    return apiRequest<ChatResponse>('/chat', {
      method: 'POST',
      body: JSON.stringify({ question }),
    });
  },

  // Get sample questions
  async getSampleQuestions(): Promise<SampleQuestionsResponse> {
    return apiRequest<SampleQuestionsResponse>('/sample-questions');
  },

  // Get conversation history
  async getHistory(): Promise<ConversationHistory> {
    return apiRequest<ConversationHistory>('/history');
  },

  // Get conversation statistics
  async getStats(): Promise<StatsResponse> {
    return apiRequest<StatsResponse>('/stats');
  },

  // Export conversation
  async exportConversation(): Promise<{ message: string; filename: string; timestamp: string }> {
    return apiRequest<{ message: string; filename: string; timestamp: string }>('/export');
  },

  // Clear conversation memory
  async clearMemory(): Promise<{ message: string; timestamp: string }> {
    return apiRequest<{ message: string; timestamp: string }>('/clear', {
      method: 'POST',
    });
  },

  // Health check
  async healthCheck(): Promise<{ status: string; chatbot_loaded: boolean; timestamp: string }> {
    return apiRequest<{ status: string; chatbot_loaded: boolean; timestamp: string }>('/health');
  },
};
