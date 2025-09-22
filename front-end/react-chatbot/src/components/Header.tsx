// Header component for the application title and description
// This is a simple presentational component

;
import './Header.css';

export function Header() {
  return (
    <div className="header">
      <h1>🇬🇷 Greek Derby Chatbot</h1>
      <p>Ask questions about Olympiakos vs Panathinaikos derby</p>
    </div>
  );
}
