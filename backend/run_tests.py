#!/usr/bin/env python3
"""
Test runner script for the Greek Derby RAG Chatbot backend.
"""
import os
import sys
import subprocess

def main():
    """Run backend tests with proper environment setup."""
    
    # Set up test environment variables
    test_env = {
        "OPENAI_API_KEY": "test-openai-key",
        "PINECONE_API_KEY": "test-pinecone-key",
        "PINECONE_GREEK_DERBY_INDEX_NAME": "test-index",
        "USER_AGENT": "test-agent",
        "PYTHONPATH": os.path.dirname(os.path.abspath(__file__))
    }
    
    # Update environment
    os.environ.update(test_env)
    
    # Add backend directory to Python path
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
    
    # Run pytest
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", 
            "-v", 
            "--tb=short",
            "--cov=.",
            "--cov-report=term-missing",
            "--cov-report=html:htmlcov"
        ], cwd=backend_dir, env=os.environ)
        
        return result.returncode
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
