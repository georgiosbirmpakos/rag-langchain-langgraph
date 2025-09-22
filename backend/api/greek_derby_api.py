#!/usr/bin/env python3
"""
FastAPI Web Server for Greek Derby RAG Chatbot
Exposes the chatbot as HTTP endpoints for easy testing and use.
"""

import os
from datetime import datetime
from typing import Dict, List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Set a default USER_AGENT to silence warnings from HTTP clients used downstream
os.environ.setdefault("USER_AGENT", "greek-derby-api/1.0")

# Import our chatbot
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "standalone-service"))
from greek_derby_chatbot import GreekDerbyChatbot


# Pydantic models for API
class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    timestamp: str
    conversation_id: Optional[str] = None


class ConversationHistory(BaseModel):
    history: List[Dict[str, str]]
    total_messages: int


class StatsResponse(BaseModel):
    total_questions: int
    total_answers: int
    conversation_start: str
    last_activity: str


# Initialize FastAPI app
app = FastAPI(
    title="Greek Derby RAG Chatbot API",
    description="API for the Greek Derby (Olympiakos vs Panathinaikos) RAG Chatbot",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global chatbot instance
chatbot = None


@app.on_event("startup")
async def startup_event():
    """Initialize the chatbot when the server starts"""
    global chatbot
    print("🚀 Starting Greek Derby RAG Chatbot API...")
    try:
        chatbot = GreekDerbyChatbot()
        print("✅ Chatbot initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize chatbot: {e}")
        raise


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "🇬🇷 Greek Derby RAG Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat - POST - Ask questions about the Greek derby",
            "history": "/history - GET - Get conversation history",
            "stats": "/stats - GET - Get conversation statistics",
            "clear": "/clear - POST - Clear conversation memory",
            "export": "/export - GET - Export conversation to JSON",
            "health": "/health - GET - Health check",
        },
        "example_questions": [
            "Ποια είναι η ιστορία του ντέρμπι;",
            "Ποιος έχει κερδίσει περισσότερες φορές;",
            "Ποιοι είναι οι κορυφαίοι παίκτες;",
            "Ποια είναι τα πιο αξέχαστα γκολ;",
            "Που γίνεται το ντέρμπι;",
        ],
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "chatbot_loaded": chatbot is not None,
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Ask a question to the chatbot"""
    if not chatbot:
        raise HTTPException(status_code=500, detail="Chatbot not initialized")

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        # Get response from chatbot
        answer = chatbot.chat(request.question)

        return ChatResponse(
            answer=answer,
            timestamp=datetime.now().isoformat(),
            conversation_id="default",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing question: {str(e)}"
        )


@app.get("/history", response_model=ConversationHistory)
async def get_history():
    """Get conversation history"""
    if not chatbot:
        raise HTTPException(status_code=500, detail="Chatbot not initialized")

    try:
        history = chatbot.get_conversation_history()
        return ConversationHistory(history=history, total_messages=len(history))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting history: {str(e)}")


@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get conversation statistics"""
    if not chatbot:
        raise HTTPException(status_code=500, detail="Chatbot not initialized")

    try:
        stats = chatbot.get_stats()
        # Parse the stats string to extract information
        lines = stats.split("\n")
        total_questions = 0
        total_answers = 0
        conversation_start = "Unknown"
        last_activity = "Unknown"

        for line in lines:
            if "Ερωτήσεις" in line:
                try:
                    total_questions = int(line.split(":")[1].strip())
                except:
                    pass
            elif "Απαντήσεις" in line:
                try:
                    total_answers = int(line.split(":")[1].strip())
                except:
                    pass
            elif "Ξεκίνησε" in line:
                conversation_start = line.split(":", 1)[1].strip()
            elif "Τελευταία" in line:
                last_activity = line.split(":", 1)[1].strip()

        return StatsResponse(
            total_questions=total_questions,
            total_answers=total_answers,
            conversation_start=conversation_start,
            last_activity=last_activity,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")


@app.post("/clear")
async def clear_memory():
    """Clear conversation memory"""
    if not chatbot:
        raise HTTPException(status_code=500, detail="Chatbot not initialized")

    try:
        chatbot.clear_memory()
        return {
            "message": "Η μνήμη της συνομιλίας διαγράφηκε.",
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing memory: {str(e)}")


@app.get("/export")
async def export_conversation():
    """Export conversation to JSON"""
    if not chatbot:
        raise HTTPException(status_code=500, detail="Chatbot not initialized")

    try:
        filename = chatbot.export_conversation()
        return {
            "message": f"Συνομιλία εξήχθη στο αρχείο: {filename}",
            "filename": filename,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error exporting conversation: {str(e)}"
        )


@app.get("/sample-questions")
async def get_sample_questions():
    """Get sample questions you can ask"""
    return {
        "sample_questions": [
            "Ποια είναι η ιστορία του ντέρμπι;",
            "Ποιος έχει κερδίσει περισσότερες φορές;",
            "Ποιοι είναι οι κορυφαίοι παίκτες;",
            "Ποια είναι τα πιο αξέχαστα γκολ;",
            "Που γίνεται το ντέρμπι;",
            "Ποια είναι η σημασία για τους φιλάθλους;",
            "Ποια είναι τα στατιστικά;",
            "Ποια είναι τα γήπεδα;",
            "Ποια είναι τα πιο αξέχαστα γεγονότα;",
            "Πώς ξεκίνησε η αντιπαλότητα;",
        ],
        "total_questions": 10,
    }


if __name__ == "__main__":
    print("🇬🇷 Starting Greek Derby RAG Chatbot API Server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("📚 API documentation at: http://localhost:8000/docs")
    print("🔍 Health check at: http://localhost:8000/health")

    uvicorn.run(
        "greek_derby_api:app", host="0.0.0.0", port=8000, reload=True, log_level="info"
    )
