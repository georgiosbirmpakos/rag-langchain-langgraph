import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import { ChatContextProvider } from '../context/ChatContext'
import Chat from '../components/Chat'

// Mock the API service
const mockSendMessage = vi.fn()
const mockGetHistory = vi.fn()

vi.mock('../services/api', () => ({
  sendMessage: mockSendMessage,
  getHistory: mockGetHistory,
  getStats: vi.fn(),
  clearHistory: vi.fn(),
  getSampleQuestions: vi.fn()
}))

describe('Chat Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders chat interface', () => {
    render(
      <ChatContextProvider>
        <Chat />
      </ChatContextProvider>
    )
    
    expect(screen.getByRole('textbox')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /send/i })).toBeInTheDocument()
  })

  it('sends message when form is submitted', async () => {
    mockSendMessage.mockResolvedValue({
      answer: 'Test response',
      sources: []
    })

    render(
      <ChatContextProvider>
        <Chat />
      </ChatContextProvider>
    )
    
    const input = screen.getByRole('textbox')
    const sendButton = screen.getByRole('button', { name: /send/i })
    
    fireEvent.change(input, { target: { value: 'Test question' } })
    fireEvent.click(sendButton)
    
    await waitFor(() => {
      expect(mockSendMessage).toHaveBeenCalledWith('Test question')
    })
  })

  it('displays loading state while sending message', async () => {
    mockSendMessage.mockImplementation(() => new Promise(resolve => 
      setTimeout(() => resolve({ answer: 'Test response', sources: [] }), 100)
    ))

    render(
      <ChatContextProvider>
        <Chat />
      </ChatContextProvider>
    )
    
    const input = screen.getByRole('textbox')
    const sendButton = screen.getByRole('button', { name: /send/i })
    
    fireEvent.change(input, { target: { value: 'Test question' } })
    fireEvent.click(sendButton)
    
    expect(screen.getByText(/sending/i)).toBeInTheDocument()
    
    await waitFor(() => {
      expect(screen.queryByText(/sending/i)).not.toBeInTheDocument()
    })
  })

  it('displays error message when API call fails', async () => {
    mockSendMessage.mockRejectedValue(new Error('API Error'))

    render(
      <ChatContextProvider>
        <Chat />
      </ChatContextProvider>
    )
    
    const input = screen.getByRole('textbox')
    const sendButton = screen.getByRole('button', { name: /send/i })
    
    fireEvent.change(input, { target: { value: 'Test question' } })
    fireEvent.click(sendButton)
    
    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument()
    })
  })
})
