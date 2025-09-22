#!/usr/bin/env python3
"""
Simple test to verify API can be imported without environment variable errors.
"""
import os
import sys

# Set up test environment variables
os.environ.update({
    "OPENAI_API_KEY": "test-openai-key",
    "PINECONE_API_KEY": "test-pinecone-key",
    "PINECONE_GREEK_DERBY_INDEX_NAME": "test-index",
    "USER_AGENT": "test-agent"
})

# Add backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

try:
    # Try to import the API module
    from api.greek_derby_api import app
    print("✅ API module imported successfully!")
    print(f"✅ App object: {app}")
    print("✅ All environment variables are properly set")
except Exception as e:
    print(f"❌ Error importing API module: {e}")
    sys.exit(1)
