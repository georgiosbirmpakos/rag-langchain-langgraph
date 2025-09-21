// SampleQuestions component for displaying clickable sample questions
// This loads questions from the API and handles clicks

import React, { useEffect } from 'react';
import { useChat } from '../context/ChatContext';
import { useSampleQuestions } from '../hooks/useApi';
import './SampleQuestions.css';

export function SampleQuestions() {
  const { sampleQuestions, loading, error, loadSampleQuestions } = useSampleQuestions();
  const { setSampleQuestions } = useChat();

  // Load sample questions on component mount
  useEffect(() => {
    loadSampleQuestions();
  }, [loadSampleQuestions]);

  // Update context when questions are loaded
  useEffect(() => {
    if (sampleQuestions.length > 0) {
      setSampleQuestions(sampleQuestions);
    }
  }, [sampleQuestions, setSampleQuestions]);

  // Handle question click
  const handleQuestionClick = (question: string) => {
    // This will be handled by the parent component
    // We'll emit a custom event or use a callback
    const event = new CustomEvent('sampleQuestionClick', { 
      detail: { question } 
    });
    window.dispatchEvent(event);
  };

  if (loading) {
    return (
      <div className="sample-questions">
        <h3>💡 Δείγμα Ερωτήσεων:</h3>
        <div className="loading-text">Φόρτωση ερωτήσεων...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="sample-questions">
        <h3>💡 Δείγμα Ερωτήσεων:</h3>
        <div className="error-text">Σφάλμα φόρτωσης ερωτήσεων</div>
      </div>
    );
  }

  return (
    <div className="sample-questions">
      <h3>💡 Δείγμα Ερωτήσεων:</h3>
      <div className="questions-container">
        {sampleQuestions.map((question, index) => (
          <button
            key={index}
            className="sample-question"
            onClick={() => handleQuestionClick(question)}
            type="button"
          >
            {question}
          </button>
        ))}
      </div>
    </div>
  );
}
