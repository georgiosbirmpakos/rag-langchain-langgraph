import { render, screen } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import App from '../App'

// Mock the API service
vi.mock('../services/api', () => ({
  sendMessage: vi.fn(),
  getHistory: vi.fn(),
  getStats: vi.fn(),
  clearHistory: vi.fn(),
  getSampleQuestions: vi.fn().mockResolvedValue({
    questions: [
      'What is the Greek Derby?',
      'Who are the main teams?',
      'What is the history?'
    ]
  }),
  apiService: {
    sendMessage: vi.fn(),
    getHistory: vi.fn(),
    getStats: vi.fn(),
    clearHistory: vi.fn(),
    getSampleQuestions: vi.fn().mockResolvedValue({
      questions: [
        'What is the Greek Derby?',
        'Who are the main teams?',
        'What is the history?'
      ]
    })
  },
  ApiError: class ApiError extends Error {
    constructor(message: string) {
      super(message)
      this.name = 'ApiError'
    }
  }
}))

describe('App', () => {
  it('renders the main application', () => {
    render(<App />)
    
    // Check if the main elements are rendered
    expect(screen.getByText(/Greek Derby Chatbot/i)).toBeInTheDocument()
    expect(screen.getByRole('textbox')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Στείλε/i })).toBeInTheDocument()
  })

  it('displays sample questions section', () => {
    render(<App />)
    
    // Check that the sample questions section is rendered
    expect(screen.getByText('💡 Δείγμα Ερωτήσεων:')).toBeInTheDocument()
  })
})
