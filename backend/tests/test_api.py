"""
Tests for the Greek Derby API endpoints.
"""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# Add tests directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock the chatbot import
with patch.dict("sys.modules", {"greek_derby_chatbot": MagicMock()}):
    # Import the mock chatbot
    from mock_chatbot import MockGreekDerbyChatbot

    # Patch the import in the API module
    with patch("api.greek_derby_api.GreekDerbyChatbot", MockGreekDerbyChatbot):
        from api.greek_derby_api import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_check(self):
        """Test that health endpoint returns 200."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"


class TestRootEndpoint:
    """Test root endpoint."""

    def test_root_endpoint(self):
        """Test that root endpoint returns API information."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data


class TestSampleQuestionsEndpoint:
    """Test sample questions endpoint."""

    def test_sample_questions(self):
        """Test that sample questions endpoint returns questions."""
        response = client.get("/sample-questions")
        assert response.status_code == 200
        data = response.json()
        assert "questions" in data
        assert isinstance(data["questions"], list)
        assert len(data["questions"]) > 0


class TestChatEndpoint:
    """Test chat endpoint with mocked RAG system."""

    @patch("api.greek_derby_api.rag_chain")
    def test_chat_success(self, mock_rag_chain):
        """Test successful chat request."""
        # Mock the RAG chain response
        mock_rag_chain.invoke.return_value = {
            "answer": "Test response about the Greek Derby",
            "source_documents": [],
        }

        response = client.post("/chat", json={"question": "What is the Greek Derby?"})

        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "sources" in data
        assert data["answer"] == "Test response about the Greek Derby"

    def test_chat_missing_question(self):
        """Test chat endpoint with missing question."""
        response = client.post("/chat", json={})
        assert response.status_code == 422  # Validation error

    def test_chat_invalid_input(self):
        """Test chat endpoint with invalid input."""
        response = client.post("/chat", json={"question": ""})
        assert response.status_code == 422  # Validation error


class TestHistoryEndpoint:
    """Test conversation history endpoint."""

    def test_history_endpoint(self):
        """Test that history endpoint returns conversation history."""
        response = client.get("/history")
        assert response.status_code == 200
        data = response.json()
        assert "history" in data
        assert isinstance(data["history"], list)


class TestStatsEndpoint:
    """Test statistics endpoint."""

    def test_stats_endpoint(self):
        """Test that stats endpoint returns statistics."""
        response = client.get("/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_messages" in data
        assert "total_questions" in data
        assert "total_answers" in data


class TestClearEndpoint:
    """Test clear conversation endpoint."""

    def test_clear_endpoint(self):
        """Test that clear endpoint clears conversation."""
        response = client.post("/clear")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "cleared" in data["message"].lower()


class TestExportEndpoint:
    """Test export conversation endpoint."""

    def test_export_endpoint(self):
        """Test that export endpoint returns conversation data."""
        response = client.get("/export")
        assert response.status_code == 200
        data = response.json()
        assert "conversation" in data
        assert "exported_at" in data
