"""
Tests for the RAG system components.
"""
import pytest
from unittest.mock import patch, MagicMock
import os

# Mock environment variables
os.environ["OPENAI_API_KEY"] = "test-key"
os.environ["PINECONE_API_KEY"] = "test-key"
os.environ["PINECONE_GREEK_DERBY_INDEX_NAME"] = "test-index"


class TestRAGSystem:
    """Test RAG system functionality."""
    
    @patch('langchain_openai.OpenAIEmbeddings')
    @patch('langchain_pinecone.PineconeVectorStore')
    @patch('langchain_openai.ChatOpenAI')
    def test_rag_initialization(self, mock_chat, mock_vector_store, mock_embeddings):
        """Test that RAG system initializes correctly."""
        # Mock the components
        mock_embeddings.return_value = MagicMock()
        mock_vector_store.return_value = MagicMock()
        mock_chat.return_value = MagicMock()
        
        # Import after mocking
        from standalone_service.greek_derby_chatbot import GreekDerbyRAG
        
        # This should not raise an exception
        rag = GreekDerbyRAG()
        assert rag is not None
    
    @patch('langchain_openai.OpenAIEmbeddings')
    @patch('langchain_pinecone.PineconeVectorStore')
    @patch('langchain_openai.ChatOpenAI')
    def test_rag_query(self, mock_chat, mock_vector_store, mock_embeddings):
        """Test RAG query functionality."""
        # Mock the components
        mock_embeddings.return_value = MagicMock()
        mock_vector_store.return_value = MagicMock()
        mock_chat.return_value = MagicMock()
        
        # Mock the chain invoke method
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = {
            "answer": "Test answer about Greek Derby",
            "source_documents": []
        }
        
        with patch('standalone_service.greek_derby_chatbot.GreekDerbyRAG._create_rag_chain', return_value=mock_chain):
            from standalone_service.greek_derby_chatbot import GreekDerbyRAG
            
            rag = GreekDerbyRAG()
            result = rag.query("What is the Greek Derby?")
            
            assert "answer" in result
            assert "sources" in result
            assert result["answer"] == "Test answer about Greek Derby"


class TestWebScraping:
    """Test web scraping functionality."""
    
    @patch('requests.get')
    def test_gazzetta_scraping(self, mock_get):
        """Test Gazzetta.gr content scraping."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <body>
                <div class="article-title">Test Article</div>
                <div class="article-content">Test content about Greek Derby</div>
            </body>
        </html>
        """
        mock_get.return_value = mock_response
        
        from scheduler.update_vector_db import scrape_gazzetta_content
        
        content = scrape_gazzetta_content("https://test.gazzetta.gr")
        
        assert content is not None
        assert len(content) > 0
    
    @patch('requests.get')
    def test_scraping_failure_handling(self, mock_get):
        """Test handling of scraping failures."""
        # Mock a failed response
        mock_get.side_effect = Exception("Network error")
        
        from scheduler.update_vector_db import scrape_gazzetta_content
        
        content = scrape_gazzetta_content("https://test.gazzetta.gr")
        
        # Should return empty content on failure
        assert content == ""


class TestVectorDatabase:
    """Test vector database operations."""
    
    @patch('pinecone.Pinecone')
    def test_pinecone_connection(self, mock_pinecone):
        """Test Pinecone connection."""
        mock_index = MagicMock()
        mock_pinecone.return_value.Index.return_value = mock_index
        
        from scheduler.update_vector_db import initialize_pinecone
        
        index = initialize_pinecone()
        
        assert index is not None
        mock_pinecone.assert_called_once()
    
    @patch('pinecone.Pinecone')
    def test_vector_upsert(self, mock_pinecone):
        """Test vector upsert operation."""
        mock_index = MagicMock()
        mock_pinecone.return_value.Index.return_value = mock_index
        
        from scheduler.update_vector_db import upsert_vectors
        
        vectors = [
            {"id": "1", "values": [0.1, 0.2, 0.3], "metadata": {"text": "test"}}
        ]
        
        upsert_vectors(mock_index, vectors)
        
        mock_index.upsert.assert_called_once()
