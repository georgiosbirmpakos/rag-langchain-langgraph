// Message component for displaying individual chat messages
// This is a pure component that handles both user and bot messages

;
import type { Message as MessageType } from '../types';
import './Message.css';

interface MessageProps {
  message: MessageType;
}

export function Message({ message }: MessageProps) {
  const { text, sender, timestamp, isError } = message;
  
  const senderName = sender === 'user' ? 'Εσείς' : 'Chatbot';
  const messageClass = `message ${sender}-message${isError ? ' error' : ''}`;

  return (
    <div className={messageClass}>
      <div className="message-header">
        <strong>{senderName}</strong>
        <small className="message-timestamp">{timestamp}</small>
      </div>
      <div className="message-content">{text}</div>
    </div>
  );
}
