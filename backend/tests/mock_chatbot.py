"""
Mock chatbot for testing purposes.
"""
from datetime import datetime
from typing import Dict, List, Optional

class MockGreekDerbyChatbot:
    """Mock chatbot that doesn't require external dependencies."""
    
    def __init__(self):
        self.conversation_history = []
        self.stats = {
            "total_messages": 0,
            "total_questions": 0,
            "total_answers": 0
        }
    
    def ask_question(self, question: str) -> Dict:
        """Mock ask_question method."""
        answer = f"Mock response to: {question}"
        
        # Update stats
        self.stats["total_messages"] += 1
        self.stats["total_questions"] += 1
        self.stats["total_answers"] += 1
        
        # Add to history
        self.conversation_history.append({
            "question": question,
            "answer": answer,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "answer": answer,
            "sources": ["Mock source 1", "Mock source 2"]
        }
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history."""
        return self.conversation_history
    
    def get_stats(self) -> Dict:
        """Get conversation statistics."""
        return self.stats
    
    def clear_memory(self) -> str:
        """Clear conversation memory."""
        self.conversation_history = []
        self.stats = {
            "total_messages": 0,
            "total_questions": 0,
            "total_answers": 0
        }
        return "Memory cleared successfully"
    
    def export_conversation(self) -> Dict:
        """Export conversation data."""
        return {
            "conversation": self.conversation_history,
            "stats": self.stats,
            "exported_at": datetime.now().isoformat()
        }
