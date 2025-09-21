"""
Configuration file for the vector database updater
"""

# Update frequency settings
UPDATE_INTERVAL_HOURS = 1  # Update every hour
CLEANUP_INTERVAL_HOURS = 24  # Clean up content older than 24 hours

# Content settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
MIN_CONTENT_LENGTH = 50  # Minimum content length to consider valid

# Gazzetta.gr URLs to scrape
GAZZETTA_URLS = [
    "https://www.gazzetta.gr/football/superleague/olympiakos",
    "https://www.gazzetta.gr/football/superleague/panathinaikos",
    "https://www.gazzetta.gr/football/superleague",
    "https://www.gazzetta.gr"
]

# CSS selectors for content extraction
CONTENT_SELECTORS = [
    "article-content", "article-title", "article-body", "content", "post-content",
    "entry-content", "post-body", "article-text", "main-content", "story-content",
    "article", "post", "content-area", "main", "body"
]

# User agent for web scraping
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Logging settings
LOG_LEVEL = "INFO"
LOG_FILE = "vector_db_updater.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Rate limiting (seconds between requests)
REQUEST_DELAY = 2

# Error handling
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds
