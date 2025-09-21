#!/usr/bin/env python3
"""
Scheduled Vector Database Updater
Updates the Pinecone vector database with fresh content from Gazzetta.gr every hour.
This script can be run as a cron job or scheduled task.
"""

import os
import sys
import time
import logging
from datetime import datetime
from typing import List, Dict, Any
import requests
import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

# Add the parent directory to the path to import the chatbot
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'standalone-service'))

class VectorDBUpdater:
    """Handles scheduled updates to the vector database with fresh Gazzetta.gr content"""
    
    def __init__(self):
        """Initialize the updater with all necessary components"""
        self.logger = self._setup_logging()
        self.logger.info("🚀 Initializing Vector Database Updater...")
        
        # Load environment variables
        self._load_environment()
        
        # Initialize components
        self._init_embeddings()
        self._init_vector_store()
        
        # Gazzetta.gr URLs to scrape
        self.greek_derby_urls = [
            "https://www.gazzetta.gr/football/superleague/olympiakos",
            "https://www.gazzetta.gr/football/superleague/panathinaikos",
            "https://www.gazzetta.gr/football/superleague",
            "https://www.gazzetta.gr"
        ]
        
        self.logger.info("✅ Vector Database Updater initialized successfully!")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # File handler with UTF-8 encoding
        file_handler = logging.FileHandler('vector_db_updater.log', encoding='utf-8')
        file_handler.setFormatter(formatter)
        
        # Console handler with UTF-8 encoding
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        
        # Configure root logger
        logging.basicConfig(
            level=logging.INFO,
            handlers=[file_handler, console_handler]
        )
        return logging.getLogger(__name__)
    
    def _load_environment(self):
        """Load environment variables"""
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            self.logger.warning("⚠️  python-dotenv not installed. Make sure to set environment variables manually.")
        
        # Check required environment variables
        required_vars = ['OPENAI_API_KEY', 'PINECONE_API_KEY', 'PINECONE_GREEK_DERBY_INDEX_NAME']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            self.logger.error(f"❌ Missing environment variables: {', '.join(missing_vars)}")
            sys.exit(1)
        
        self.logger.info("✅ Environment variables loaded")
    
    def _init_embeddings(self):
        """Initialize embeddings model"""
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            dimensions=1024
        )
        self.logger.info("✅ Embeddings model initialized")
    
    def _init_vector_store(self):
        """Initialize vector store connection"""
        pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
        self.index = pc.Index(os.getenv('PINECONE_GREEK_DERBY_INDEX_NAME'))
        self.vector_store = PineconeVectorStore(embedding=self.embeddings, index=self.index)
        self.logger.info("✅ Vector store initialized")
    
    def load_fresh_content(self) -> List[Document]:
        """Load fresh content from Gazzetta.gr"""
        self.logger.info("📚 Loading fresh content from Gazzetta.gr...")
        
        # Set user agent to avoid blocking
        os.environ['USER_AGENT'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        
        all_docs = []
        successful_urls = []
        
        for url in self.greek_derby_urls:
            try:
                self.logger.info(f"Loading: {url}")
                
                # Try with CSS selectors first
                loader = WebBaseLoader(
                    web_paths=(url,),
                    bs_kwargs=dict(
                        parse_only=bs4.SoupStrainer(
                            class_=("article-content", "article-title", "article-body", "content", "post-content", 
                                   "entry-content", "post-body", "article-text", "main-content", "story-content",
                                   "article", "post", "content-area", "main", "body")
                        )
                    ),
                )
                docs = loader.load()
                
                # If no content found, try without selectors
                if not docs or all(len(doc.page_content.strip()) < 100 for doc in docs):
                    self.logger.info(f"  No content found with selectors, trying without filtering...")
                    loader_fallback = WebBaseLoader(web_paths=(url,))
                    docs = loader_fallback.load()
                
                # Filter out very short documents
                valid_docs = [doc for doc in docs if len(doc.page_content.strip()) > 50]
                
                if valid_docs:
                    all_docs.extend(valid_docs)
                    successful_urls.append(url)
                    self.logger.info(f"  ✅ Found {len(valid_docs)} valid documents from {url}")
                else:
                    self.logger.warning(f"  ⚠️  No valid content found from {url}")
                
                # Be respectful to the server
                time.sleep(2)
                
            except Exception as e:
                self.logger.error(f"❌ Error loading {url}: {e}")
                continue
        
        # If still no content, try fallback approach
        if len(all_docs) == 0 or all(len(doc.page_content.strip()) < 100 for doc in all_docs):
            self.logger.warning("⚠️  Trying fallback approach with requests...")
            try:
                response = requests.get("https://www.gazzetta.gr/football/superleague", 
                                      headers={'User-Agent': os.environ['USER_AGENT']})
                if response.status_code == 200:
                    fallback_doc = Document(
                        page_content=response.text,
                        metadata={"source": "https://www.gazzetta.gr/football/superleague", "method": "requests"}
                    )
                    all_docs.append(fallback_doc)
                    successful_urls.append("https://www.gazzetta.gr/football/superleague")
                    self.logger.info("✅ Added fallback document from requests")
            except Exception as e:
                self.logger.error(f"❌ Fallback approach also failed: {e}")
        
        self.logger.info(f"📚 Loaded {len(all_docs)} documents from {len(successful_urls)} URLs")
        return all_docs
    
    def process_and_store_content(self, docs: List[Document]) -> int:
        """Process documents and store them in the vector database"""
        if not docs:
            self.logger.warning("⚠️  No documents to process")
            return 0
        
        self.logger.info("🔄 Processing and storing content...")
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""]
        )
        
        splits = text_splitter.split_documents(docs)
        
        # Add metadata to identify the source and update time
        current_time = datetime.now().isoformat()
        for split in splits:
            if "source" not in split.metadata:
                split.metadata["source"] = "gazzetta.gr"
            split.metadata["type"] = "greek_derby_news"
            split.metadata["updated_at"] = current_time
            split.metadata["update_batch"] = f"batch_{int(time.time())}"
        
        # Store in vector database
        try:
            self.vector_store.add_documents(splits)
            self.logger.info(f"✅ Successfully stored {len(splits)} chunks in vector database")
            return len(splits)
        except Exception as e:
            self.logger.error(f"❌ Error storing documents: {e}")
            return 0
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get current database statistics"""
        try:
            stats = self.index.describe_index_stats()
            return {
                "total_vectors": stats.get('total_vector_count', 0),
                "dimension": stats.get('dimension', 0),
                "index_fullness": stats.get('index_fullness', 0),
                "namespaces": stats.get('namespaces', {})
            }
        except Exception as e:
            self.logger.error(f"❌ Error getting database stats: {e}")
            return {}
    
    def cleanup_old_content(self, hours_threshold: int = 24):
        """Clean up content older than specified hours (optional)"""
        # Note: This is a placeholder. Pinecone doesn't have built-in TTL for metadata
        # You would need to implement this based on your specific requirements
        self.logger.info(f"🧹 Cleanup not implemented yet. Would clean content older than {hours_threshold} hours")
        pass
    
    def run_update(self) -> bool:
        """Run a complete update cycle"""
        start_time = time.time()
        self.logger.info("🔄 Starting vector database update cycle...")
        
        try:
            # Get current stats
            stats_before = self.get_database_stats()
            self.logger.info(f"📊 Database stats before update: {stats_before}")
            
            # Load fresh content
            docs = self.load_fresh_content()
            
            if not docs:
                self.logger.error("❌ No content loaded. Update failed.")
                return False
            
            # Process and store content
            chunks_added = self.process_and_store_content(docs)
            
            if chunks_added == 0:
                self.logger.error("❌ No chunks were added. Update failed.")
                return False
            
            # Get updated stats
            stats_after = self.get_database_stats()
            self.logger.info(f"📊 Database stats after update: {stats_after}")
            
            # Calculate duration
            duration = time.time() - start_time
            self.logger.info(f"✅ Update completed successfully in {duration:.2f} seconds")
            self.logger.info(f"📈 Added {chunks_added} new chunks to the database")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Update failed with error: {e}")
            return False

def main():
    """Main function to run the updater"""
    updater = VectorDBUpdater()
    
    # Run the update
    success = updater.run_update()
    
    if success:
        print("✅ Vector database update completed successfully!")
        sys.exit(0)
    else:
        print("❌ Vector database update failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
