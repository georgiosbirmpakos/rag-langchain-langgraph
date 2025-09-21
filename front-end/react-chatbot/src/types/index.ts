// TypeScript type definitions for our chatbot application
// This ensures type safety throughout our application

export interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: string;
  isError?: boolean;
}

export interface ChatState {
  messages: Message[];
  isLoading: boolean;
  sampleQuestions: string[];
  error: string | null;
}

export interface ChatResponse {
  answer: string;
  timestamp: string;
  conversation_id?: string;
}

export interface SampleQuestionsResponse {
  sample_questions: string[];
  total_questions: number;
}

export interface ConversationHistory {
  history: Array<{ role: string; content: string }>;
  total_messages: number;
}

export interface StatsResponse {
  total_questions: number;
  total_answers: number;
  conversation_start: string;
  last_activity: string;
}

// API configuration
export const API_BASE = 'http://localhost:8000';
