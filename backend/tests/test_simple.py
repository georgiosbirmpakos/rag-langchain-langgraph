"""
Simple tests that don't require complex imports.
"""

import os

import pytest


def test_environment_variables():
    """Test that environment variables are set correctly."""
    assert os.environ.get("OPENAI_API_KEY") is not None
    assert os.environ.get("PINECONE_API_KEY") is not None
    assert os.environ.get("PINECONE_GREEK_DERBY_INDEX_NAME") is not None
    assert os.environ.get("USER_AGENT") is not None


def test_mock_chatbot():
    """Test the mock chatbot functionality."""
    from mock_chatbot import MockGreekDerbyChatbot

    chatbot = MockGreekDerbyChatbot()

    # Test asking a question
    response = chatbot.ask_question("What is the Greek Derby?")
    assert "answer" in response
    assert "sources" in response
    assert "Mock response to: What is the Greek Derby?" in response["answer"]

    # Test stats
    stats = chatbot.get_stats()
    assert stats["total_questions"] == 1
    assert stats["total_answers"] == 1

    # Test history
    history = chatbot.get_conversation_history()
    assert len(history) == 1
    assert history[0]["question"] == "What is the Greek Derby?"


def test_mock_chatbot_clear():
    """Test clearing chatbot memory."""
    from mock_chatbot import MockGreekDerbyChatbot

    chatbot = MockGreekDerbyChatbot()

    # Ask a question first
    chatbot.ask_question("Test question")
    assert chatbot.get_stats()["total_questions"] == 1

    # Clear memory
    result = chatbot.clear_memory()
    assert "cleared" in result.lower()
    assert chatbot.get_stats()["total_questions"] == 0
    assert len(chatbot.get_conversation_history()) == 0


def test_mock_chatbot_export():
    """Test exporting conversation data."""
    from mock_chatbot import MockGreekDerbyChatbot

    chatbot = MockGreekDerbyChatbot()
    chatbot.ask_question("Test question")

    export_data = chatbot.export_conversation()
    assert "conversation" in export_data
    assert "stats" in export_data
    assert "exported_at" in export_data
    assert len(export_data["conversation"]) == 1
