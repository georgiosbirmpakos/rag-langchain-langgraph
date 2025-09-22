import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
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
  })
}))

describe('App', () => {
  it('renders the main application', () => {
    render(<App />)
    
    // Check if the main elements are rendered
    expect(screen.getByText(/Greek Derby Chatbot/i)).toBeInTheDocument()
    expect(screen.getByRole('textbox')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /send/i })).toBeInTheDocument()
  })

  it('displays sample questions', async () => {
    render(<App />)
    
    // Wait for sample questions to load
    await screen.findByText('What is the Greek Derby?')
    expect(screen.getByText('Who are the main teams?')).toBeInTheDocument()
    expect(screen.getByText('What is the history?')).toBeInTheDocument()
  })
})
