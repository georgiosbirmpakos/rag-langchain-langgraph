// Main Chat component that orchestrates all chat functionality
// This is the central component that brings everything together

import { useEffect } from 'react';
import { useChat } from '../context/ChatContext';
import { useScrollToBottom } from '../hooks/useScrollToBottom';
import { Message } from './Message';
import { ChatInput } from './ChatInput';
import { SampleQuestions } from './SampleQuestions';
import './Chat.css';

export function Chat() {
  const { state } = useChat();
  const { messages, isLoading, error } = state;
  const {
    scrollContainerRef,
    showScrollButton,
    scrollToBottom,
    autoScrollIfNeeded,
  } = useScrollToBottom();

  // Auto-scroll when new messages are added
  useEffect(() => {
    autoScrollIfNeeded();
  }, [messages, autoScrollIfNeeded]);

  // Handle sample question clicks
  useEffect(() => {
    const handleSampleQuestionClick = (event: CustomEvent) => {
      const { question } = event.detail;
      // Trigger the input with the question
      const input = document.querySelector('.message-input') as HTMLInputElement;
      if (input) {
        input.value = question;
        input.focus();
        // Trigger the form submission
        const form = input.closest('form');
        if (form) {
          form.requestSubmit();
        }
      }
    };

    window.addEventListener('sampleQuestionClick', handleSampleQuestionClick as EventListener);
    
    return () => {
      window.removeEventListener('sampleQuestionClick', handleSampleQuestionClick as EventListener);
    };
  }, []);

  return (
    <div className="chat-container">
      <div className="chat-messages" ref={scrollContainerRef}>
        {messages.map((message) => (
          <Message key={message.id} message={message} />
        ))}
        
        {isLoading && (
          <div className="loading-message">
            ⏳ Απαντάω στην ερώτησή σας...
          </div>
        )}
        
        {error && (
          <div className="error-message">
            ❌ {error}
          </div>
        )}
      </div>
      
      {showScrollButton && (
        <button
          className="scroll-button"
          onClick={scrollToBottom}
          title="Πήγαινε στο κάτω μέρος"
          type="button"
        >
          ⬇️
        </button>
      )}
      
      <ChatInput />
      <SampleQuestions />
    </div>
  );
}
