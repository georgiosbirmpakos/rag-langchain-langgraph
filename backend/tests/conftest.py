"""
Pytest configuration and fixtures for backend tests.
"""
import os
import sys
from unittest.mock import patch, MagicMock

# Set up test environment variables
os.environ.update({
    "OPENAI_API_KEY": "test-openai-key",
    "PINECONE_API_KEY": "test-pinecone-key", 
    "PINECONE_GREEK_DERBY_INDEX_NAME": "test-index",
    "USER_AGENT": "test-agent",
    "PYTHONPATH": os.path.join(os.path.dirname(__file__), "..")
})

# Mock all external dependencies before any imports
mock_modules = {
    'langchain_openai': MagicMock(),
    'langchain_pinecone': MagicMock(),
    'langchain_core': MagicMock(),
    'langchain_community': MagicMock(),
    'langgraph': MagicMock(),
    'pinecone': MagicMock(),
    'requests': MagicMock(),
    'beautifulsoup4': MagicMock(),
    'python-dotenv': MagicMock(),
    'greek_derby_chatbot': MagicMock()
}

# Apply mocks globally
for module_name, mock_module in mock_modules.items():
    sys.modules[module_name] = mock_module

# Import mock chatbot
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mock_chatbot import MockGreekDerbyChatbot

# Configure pytest
import pytest

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up test environment for each test."""
    # Ensure environment variables are set
    test_env = {
        "OPENAI_API_KEY": "test-openai-key",
        "PINECONE_API_KEY": "test-pinecone-key",
        "PINECONE_GREEK_DERBY_INDEX_NAME": "test-index",
        "USER_AGENT": "test-agent"
    }
    
    for key, value in test_env.items():
        os.environ[key] = value
    
    yield
    
    # Cleanup after test
    for key in test_env.keys():
        if key in os.environ:
            del os.environ[key]

@pytest.fixture
def mock_rag_chain():
    """Mock RAG chain for testing."""
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = {
        "answer": "Test response about Greek Derby",
        "source_documents": []
    }
    return mock_chain

@pytest.fixture
def mock_vector_store():
    """Mock vector store for testing."""
    mock_store = MagicMock()
    mock_store.similarity_search.return_value = []
    return mock_store

@pytest.fixture
def mock_embeddings():
    """Mock embeddings for testing."""
    mock_embeddings = MagicMock()
    mock_embeddings.embed_documents.return_value = [[0.1, 0.2, 0.3]]
    mock_embeddings.embed_query.return_value = [0.1, 0.2, 0.3]
    return mock_embeddings
