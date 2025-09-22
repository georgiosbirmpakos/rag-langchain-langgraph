// React Context for global chat state management
// This provides a clean way to share state across components without prop drilling

import { createContext, useContext, useReducer, type ReactNode } from 'react';
import type { Message, ChatState } from '../types';

// Action types for the reducer
type ChatAction =
  | { type: 'ADD_MESSAGE'; payload: Message }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_SAMPLE_QUESTIONS'; payload: string[] }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'CLEAR_MESSAGES' }
  | { type: 'CLEAR_ERROR' };

// Initial state
const initialState: ChatState = {
  messages: [
    {
      id: 'welcome',
      text: 'Γεια σας! Είμαι ο βοηθός για το ελληνικό ντέρμπι Ολυμπιακός-Παναθηναϊκός. Πώς μπορώ να σας βοηθήσω σήμερα;',
      sender: 'bot',
      timestamp: new Date().toLocaleTimeString('el-GR', { 
        hour: '2-digit', 
        minute: '2-digit' 
      }),
    }
  ],
  isLoading: false,
  sampleQuestions: [],
  error: null,
};

// Reducer function
function chatReducer(state: ChatState, action: ChatAction): ChatState {
  switch (action.type) {
    case 'ADD_MESSAGE':
      return {
        ...state,
        messages: [...state.messages, action.payload],
        error: null, // Clear error when adding a new message
      };
    
    case 'SET_LOADING':
      return {
        ...state,
        isLoading: action.payload,
      };
    
    case 'SET_SAMPLE_QUESTIONS':
      return {
        ...state,
        sampleQuestions: action.payload,
      };
    
    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload,
        isLoading: false,
      };
    
    case 'CLEAR_MESSAGES':
      return {
        ...state,
        messages: [initialState.messages[0]], // Keep welcome message
        error: null,
      };
    
    case 'CLEAR_ERROR':
      return {
        ...state,
        error: null,
      };
    
    default:
      return state;
  }
}

// Context type
interface ChatContextType {
  state: ChatState;
  dispatch: React.Dispatch<ChatAction>;
  addMessage: (text: string, sender: 'user' | 'bot', isError?: boolean) => void;
  setLoading: (loading: boolean) => void;
  setSampleQuestions: (questions: string[]) => void;
  setError: (error: string | null) => void;
  clearMessages: () => void;
  clearError: () => void;
}

// Create context
const ChatContext = createContext<ChatContextType | undefined>(undefined);

// Provider component
interface ChatProviderProps {
  children: ReactNode;
}

export function ChatProvider({ children }: ChatProviderProps) {
  const [state, dispatch] = useReducer(chatReducer, initialState);

  // Action creators
  const addMessage = (text: string, sender: 'user' | 'bot', isError = false) => {
    const message: Message = {
      id: Date.now().toString(),
      text,
      sender,
      timestamp: new Date().toLocaleTimeString('el-GR', { 
        hour: '2-digit', 
        minute: '2-digit' 
      }),
      isError,
    };
    dispatch({ type: 'ADD_MESSAGE', payload: message });
  };

  const setLoading = (loading: boolean) => {
    dispatch({ type: 'SET_LOADING', payload: loading });
  };

  const setSampleQuestions = (questions: string[]) => {
    dispatch({ type: 'SET_SAMPLE_QUESTIONS', payload: questions });
  };

  const setError = (error: string | null) => {
    dispatch({ type: 'SET_ERROR', payload: error });
  };

  const clearMessages = () => {
    dispatch({ type: 'CLEAR_MESSAGES' });
  };

  const clearError = () => {
    dispatch({ type: 'CLEAR_ERROR' });
  };

  const value: ChatContextType = {
    state,
    dispatch,
    addMessage,
    setLoading,
    setSampleQuestions,
    setError,
    clearMessages,
    clearError,
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
}

// Custom hook to use the context
export function useChat() {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
}
