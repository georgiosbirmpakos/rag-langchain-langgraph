# 🇬🇷 Greek Derby RAG Chatbot - Backend

A sophisticated RAG (Retrieval-Augmented Generation) chatbot system that provides real-time information about the Greek football derby between Olympiakos and Panathinaikos, powered by content from [Gazzetta.gr](https://www.gazzetta.gr/).

## 🚀 Features

### **Real-time Content Integration**
- **Gazzetta.gr Scraping**: Automatically fetches latest news and information from Greece's premier sports website
- **Multi-source Data**: Loads content from Olympiakos, Panathinaikos, and general Super League pages
- **Intelligent Fallback**: Falls back to sample content if web scraping fails
- **Respectful Scraping**: Implements delays and proper user agents to respect the website

### **Advanced RAG Architecture**
- **Vector Database**: Uses Pinecone for efficient similarity search
- **OpenAI Integration**: GPT-4o-mini for intelligent responses
- **Embeddings**: text-embedding-3-small for high-quality vector representations
- **LangGraph**: Sophisticated graph-based RAG pipeline
- **Memory System**: Conversation history and context awareness

### **API Endpoints**
- **FastAPI Backend**: Modern, fast API with automatic documentation
- **CORS Support**: Ready for frontend integration
- **Health Monitoring**: Built-in health checks and status endpoints
- **Export Functionality**: Conversation export and statistics

## 🏗️ Architecture

```
Backend/
├── api/
│   └── greek_derby_api.py          # FastAPI web server
├── standalone-service/
│   └── greek_derby_chatbot.py      # Core RAG chatbot
└── README.md                       # This file
```

### **Core Components**

1. **GreekDerbyChatbot** (`standalone-service/`)
   - Main RAG system with LangGraph
   - Gazzetta.gr content loading
   - Conversation memory management
   - Vector database operations

2. **FastAPI Server** (`api/`)
   - RESTful API endpoints
   - CORS middleware
   - Error handling
   - Request/response models

## 📋 Prerequisites

### **Required Environment Variables**
Create a `.env` file in the project root with:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_GREEK_DERBY_INDEX_NAME=your_index_name_here

# Optional: User Agent for web scraping
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
```

### **Python Dependencies**
```bash
pip install -r requirements_api.txt
```

### **Required Packages**
- `langchain` - RAG framework
- `langchain-openai` - OpenAI integration
- `langchain-pinecone` - Vector database
- `langchain-community` - Web scraping
- `langgraph` - Graph-based RAG
- `fastapi` - Web API framework
- `uvicorn` - ASGI server
- `pinecone-client` - Vector database client
- `beautifulsoup4` - HTML parsing
- `requests` - HTTP requests
- `python-dotenv` - Environment variables

## 🚀 Quick Start

### **1. Standalone Chatbot**
```bash
cd backend/standalone-service
python greek_derby_chatbot.py
```

### **2. API Server**
```bash
cd backend/api
python greek_derby_api.py
```

### **3. Using uvicorn directly**
```bash
cd backend/api
uvicorn greek_derby_api:app --host 0.0.0.0 --port 8000 --reload
```

## 📡 API Endpoints

### **Core Endpoints**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information and available endpoints |
| `GET` | `/health` | Health check and system status |
| `POST` | `/chat` | Send message to chatbot |
| `GET` | `/history` | Get conversation history |
| `GET` | `/stats` | Get conversation statistics |
| `POST` | `/clear` | Clear conversation memory |
| `GET` | `/export` | Export conversation to JSON |
| `GET` | `/sample-questions` | Get sample questions |

### **Example API Usage**

```python
import requests

# Send a message
response = requests.post('http://localhost:8000/chat', 
                        json={'question': 'Ποια είναι η ιστορία του ντέρμπι;'})
print(response.json())

# Get conversation history
history = requests.get('http://localhost:8000/history')
print(history.json())

# Get statistics
stats = requests.get('http://localhost:8000/stats')
print(stats.json())
```

## 🔄 Gazzetta.gr Integration

### **Content Sources**
The system automatically loads content from:

1. **Olympiakos Page**: `https://www.gazzetta.gr/football/superleague/olympiakos`
2. **Panathinaikos Page**: `https://www.gazzetta.gr/football/superleague/panathinaikos`
3. **Super League Page**: `https://www.gazzetta.gr/football/superleague`
4. **Main Gazzetta Page**: `https://www.gazzetta.gr`

### **Content Processing**
- **Smart Scraping**: Uses multiple CSS selectors to extract relevant content
- **Fallback Methods**: If primary scraping fails, tries alternative approaches
- **Content Filtering**: Removes short or irrelevant content
- **Greek-friendly Splitting**: Uses Greek language separators for optimal chunking
- **Metadata Enrichment**: Adds source URLs and content type information

### **Scraping Strategy**
```python
# Primary method: WebBaseLoader with CSS selectors
loader = WebBaseLoader(
    web_paths=(url,),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("article-content", "article-title", "content", ...)
        )
    ),
)

# Fallback method: No selectors
loader_fallback = WebBaseLoader(web_paths=(url,))

# Last resort: Direct requests
response = requests.get(url, headers={'User-Agent': user_agent})
```

## 🧠 RAG System Details

### **Vector Database**
- **Provider**: Pinecone
- **Embeddings**: OpenAI text-embedding-3-small (1024 dimensions)
- **Chunk Size**: 500 characters with 100 character overlap
- **Similarity Search**: Retrieves top 4 most relevant chunks

### **Language Model**
- **Model**: GPT-4o-mini
- **Provider**: OpenAI
- **Temperature**: Default (balanced creativity/consistency)
- **Max Tokens**: Context-dependent

### **Prompt Engineering**
```python
prompt_template = """
Είστε ένας εξειδικευμένος βοηθός για το ελληνικό ποδόσφαιρο και το ντέρμπι Ολυμπιακός-Παναθηναϊκός.

Χρησιμοποιήστε τις παρακάτω πληροφορίες για να απαντήσετε στην ερώτηση του χρήστη.
Αν δεν γνωρίζετε την απάντηση, πείτε ότι δεν γνωρίζετε.
Απαντήστε στα ελληνικά με φιλικό και ενημερωτικό τρόπο.
Κρατήστε τις απαντήσεις συνοπτικές αλλά πλήρεις.

Περιεχόμενο: {context}
Ερώτηση: {question}
Απάντηση:"""
```

## 🔧 Configuration

### **Environment Variables**

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for LLM and embeddings | ✅ |
| `PINECONE_API_KEY` | Pinecone API key for vector database | ✅ |
| `PINECONE_GREEK_DERBY_INDEX_NAME` | Pinecone index name | ✅ |
| `USER_AGENT` | User agent for web scraping | ❌ |

### **Customization Options**

```python
# Chunk size and overlap
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,        # Adjust based on content
    chunk_overlap=100,     # Adjust for context preservation
    separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""]
)

# Number of retrieved documents
retrieved_docs = vector_store.similarity_search(
    question, 
    k=4  # Adjust based on needs
)

# Embedding dimensions
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    dimensions=1024  # Can be 1536 or 3072
)
```

## 🐛 Troubleshooting

### **Common Issues**

1. **"No knowledge base found"**
   - **Cause**: Pinecone index is empty
   - **Solution**: The system will automatically load Gazzetta.gr content

2. **"Failed to load content from Gazzetta.gr"**
   - **Cause**: Network issues or website changes
   - **Solution**: System falls back to sample content automatically

3. **"Missing environment variables"**
   - **Cause**: Required API keys not set
   - **Solution**: Check your `.env` file and environment variables

4. **"Import errors"**
   - **Cause**: Missing dependencies
   - **Solution**: Run `pip install -r requirements_api.txt`

### **Debug Mode**
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check Pinecone index stats
stats = index.describe_index_stats()
print(f"Total vectors: {stats['total_vector_count']}")
```

## 📊 Performance

### **Expected Performance**
- **Initial Load**: 30-60 seconds (depends on Gazzetta.gr response time)
- **Query Response**: 2-5 seconds per question
- **Memory Usage**: ~200-500MB depending on content size
- **Vector Storage**: ~1-5MB for typical content

### **Optimization Tips**
- Use smaller chunk sizes for faster retrieval
- Adjust `k` parameter for similarity search
- Monitor Pinecone usage and costs
- Consider caching for frequently asked questions

## 🔒 Security

### **API Security**
- **CORS**: Configured for frontend integration
- **Input Validation**: Pydantic models for request validation
- **Error Handling**: Graceful error responses without sensitive data

### **Data Privacy**
- **No Personal Data**: System doesn't store personal information
- **Conversation History**: Stored locally, not in external databases
- **API Keys**: Use environment variables, never hardcode

## 🤝 Contributing

### **Adding New Content Sources**
1. Add URLs to `greek_derby_urls` list
2. Test scraping with new selectors if needed
3. Update metadata handling if required

### **Improving Prompts**
1. Modify prompt templates in `_init_rag_system()`
2. Test with various question types
3. Consider adding few-shot examples

### **Enhancing Scraping**
1. Add new CSS selectors for better content extraction
2. Implement content filtering for better quality
3. Add support for other Greek sports websites

## 📚 Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Gazzetta.gr](https://www.gazzetta.gr/) - Source website

