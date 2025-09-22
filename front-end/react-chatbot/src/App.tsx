// Main App component - the root of our React application
// This sets up the context provider and renders the main layout

;
import { ChatProvider } from './context/ChatContext';
import { Header } from './components/Header';
import { Chat } from './components/Chat';
import './App.css';

function App() {
  return (
    <ChatProvider>
      <div className="container">
        <Header />
        <Chat />
      </div>
    </ChatProvider>
  );
}

export default App;
