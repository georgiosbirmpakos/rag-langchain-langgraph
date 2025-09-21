// ChatInput component for message input and sending
// This handles user input, Enter key, and send button functionality

import React, { useState, useCallback } from 'react';
import { useChat } from '../context/ChatContext';
import { useSendMessage } from '../hooks/useApi';
import './ChatInput.css';

export function ChatInput() {
  const [inputValue, setInputValue] = useState('');
  const { addMessage, setLoading, setError } = useChat();
  const { sendMessage, loading, error } = useSendMessage();

  // Handle form submission
  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault();
    
    const message = inputValue.trim();
    if (!message || loading) return;

    // Add user message immediately
    addMessage(message, 'user');
    setInputValue('');
    setLoading(true);

    try {
      const response = await sendMessage(message);
      addMessage(response.answer, 'bot');
    } catch (err) {
      const errorMessage = error || 'Σφάλμα σύνδεσης';
      addMessage(errorMessage, 'bot', true);
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  }, [inputValue, loading, addMessage, setLoading, setError, sendMessage, error]);

  // Handle Enter key press
  const handleKeyPress = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  }, [handleSubmit]);

  // Handle input change
  const handleInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  }, []);

  return (
    <div className="input-container">
      <form onSubmit={handleSubmit} className="input-form">
        <input
          type="text"
          className="message-input"
          placeholder="Ρωτήστε για το ντέρμπι..."
          value={inputValue}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          disabled={loading}
        />
        <button
          type="submit"
          className="send-button"
          disabled={loading || !inputValue.trim()}
        >
          📤 Στείλε
        </button>
      </form>
    </div>
  );
}
