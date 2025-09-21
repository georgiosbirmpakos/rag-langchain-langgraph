// Custom hook for API calls with loading states and error handling
// This follows modern React patterns with proper cleanup and state management

import { useState, useCallback } from 'react';
import { apiService, ApiError } from '../services/api';
import type { ChatResponse, SampleQuestionsResponse } from '../types';

// Generic hook for API calls
function useApiCall<T>() {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const execute = useCallback(async (apiCall: () => Promise<T>) => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await apiCall();
      setData(result);
      return result;
    } catch (err) {
      const errorMessage = err instanceof ApiError 
        ? err.message 
        : 'An unexpected error occurred';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setData(null);
    setError(null);
    setLoading(false);
  }, []);

  return { data, loading, error, execute, reset };
}

// Specific hook for sending messages
export function useSendMessage() {
  const { data, loading, error, execute } = useApiCall<ChatResponse>();

  const sendMessage = useCallback(async (question: string) => {
    return execute(() => apiService.sendMessage(question));
  }, [execute]);

  return { 
    response: data, 
    loading, 
    error, 
    sendMessage 
  };
}

// Hook for loading sample questions
export function useSampleQuestions() {
  const { data, loading, error, execute } = useApiCall<SampleQuestionsResponse>();

  const loadSampleQuestions = useCallback(async () => {
    return execute(() => apiService.getSampleQuestions());
  }, [execute]);

  return { 
    sampleQuestions: data?.sample_questions || [], 
    loading, 
    error, 
    loadSampleQuestions 
  };
}

// Hook for health check
export function useHealthCheck() {
  const { data, loading, error, execute } = useApiCall<{ status: string; chatbot_loaded: boolean; timestamp: string }>();

  const checkHealth = useCallback(async () => {
    return execute(() => apiService.healthCheck());
  }, [execute]);

  return { 
    health: data, 
    loading, 
    error, 
    checkHealth 
  };
}
