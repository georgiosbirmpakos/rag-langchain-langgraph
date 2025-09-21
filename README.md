# Greek Derby RAG Chatbot 🇬🇷⚽

An interactive chatbot about the Olympiakos vs Panathinaikos derby using RAG (Retrieval-Augmented Generation) with memory. Available as a standalone application, Jupyter notebook, and web API.

## 🌟 Features

- 🤖 **Interactive Chat**: Real-time conversation about the Greek derby
- 🧠 **Memory**: Remembers conversation history across sessions
- 📚 **RAG System**: Retrieves relevant information from knowledge base
- 🇬🇷 **Greek Language**: Fully supports Greek language with proper prompts
- 💾 **Export**: Save conversations to JSON files
- 📊 **Statistics**: View conversation analytics
- 🌐 **Web API**: FastAPI-based REST API for web integration
- 📱 **Web Client**: Fullscreen HTML client for browser-based chat
- 📓 **Jupyter Notebook**: Interactive development and testing environment
- 🔧 **MCP Server**: Model Context Protocol server for AI tool integration

## 🚀 Quick Start

### Option 1: Web API (Recommended)

1. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn python-multipart
   ```

2. **Configure environment:**
   Create a `.env` file with your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   PINECONE_API_KEY=your_pinecone_api_key_here
   PINECONE_GREEK_DERBY_INDEX_NAME=your_index_name
   ```

3. **Start the API server:**
   ```bash
   python greek_derby_api.py
   ```

4. **Open the web client:**
   - Open `chatbot_web_client.html` in your browser
   - Or visit `http://localhost:8000` for API documentation

### Option 2: Standalone Application

```bash
python greek_derby_chatbot.py
```

### Option 3: Jupyter Notebook

```bash
jupyter notebook greek-derby-rag.ipynb
```

## 📁 Project Structure

```
rag-langchain-langgraph/
├── greek_derby_api.py              # FastAPI web server
├── chatbot_web_client.html         # Fullscreen web client
├── greek_derby_chatbot.py          # Standalone chatbot application
├── greek-derby-rag.ipynb           # Jupyter notebook for development
├── requirements_api.txt            # Web API dependencies
├── README.md                       # This documentation
└── .env                           # Environment variables (create this)
```

## 🌐 Web API Endpoints

### Chat Endpoints
- `POST /chat` - Ask questions to the chatbot
- `GET /history` - Get conversation history
- `GET /stats` - Get conversation statistics
- `POST /clear` - Clear conversation memory
- `GET /export` - Export conversation to JSON

### Utility Endpoints
- `GET /` - API information and sample questions
- `GET /health` - Health check
- `GET /sample-questions` - Get sample questions

### Example API Usage

```bash
# Ask a question
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"question": "Ποια είναι η ιστορία του ντέρμπι;"}'

# Get conversation history
curl "http://localhost:8000/history"

# Get statistics
curl "http://localhost:8000/stats"
```

## 💻 Usage Examples

### Interactive Commands (Standalone App)

- Ask any question about the derby in Greek
- `ιστορικό` - Show conversation history
- `διαγραφή` - Clear memory
- `στατιστικά` - Show statistics
- `εξαγωγή` - Export conversation
- `βοήθεια` - Show help
- `έξοδος` - Exit

### Sample Questions

- "Ποια είναι η ιστορία του ντέρμπι;"
- "Ποιος έχει κερδίσει περισσότερες φορές;"
- "Ποιοι είναι οι κορυφαίοι παίκτες;"
- "Ποια είναι τα πιο αξέχαστα γκολ;"
- "Που γίνεται το ντέρμπι;"
- "Ποια είναι η σημασία για τους φιλάθλους;"
- "Ποια είναι τα στατιστικά;"
- "Ποια είναι τα γήπεδα;"

## 🏗️ Architecture

### Core Components

1. **Language Model**: GPT-4o-mini for Greek language support
2. **Embeddings**: OpenAI text-embedding-3-small for Greek text
3. **Vector Store**: Pinecone for document storage and retrieval
4. **RAG System**: LangGraph-based retrieval and generation
5. **Memory**: ConversationBufferMemory for context awareness
6. **Web Framework**: FastAPI for REST API
7. **Frontend**: HTML/CSS/JavaScript for web client

### Knowledge Base

The chatbot includes a comprehensive knowledge base about:
- Derby history and statistics
- Key players and moments
- Stadium information
- Fan culture and significance
- Memorable goals and events
- Rivalry origins and development

### Data Sources

- **Primary**: Web scraping from www.gazzetta.gr
- **Fallback**: Sample knowledge base with curated content
- **Vector Storage**: Pinecone index for semantic search

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_GREEK_DERBY_INDEX_NAME=your_index_name

# Optional
USER_AGENT=greek-derby-chatbot/1.0
```

### Pinecone Setup

1. Create a Pinecone account at [pinecone.io](https://pinecone.io)
2. Create a new index with:
   - Name: `greek-derby-index` (or your preferred name)
   - Dimensions: 1536 (for OpenAI embeddings)
   - Metric: cosine

## 📱 Web Client Features

### Fullscreen Interface
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Smooth Scrolling**: Auto-scrolls as conversation grows
- **Message Timestamps**: Shows when each message was sent
- **Sample Questions**: Click to try pre-made questions
- **Error Handling**: Shows connection errors gracefully

### Interactive Elements
- **Real-time Chat**: Instant responses from the API
- **Scroll Controls**: Button to jump to latest messages
- **Loading Indicators**: Shows when processing requests
- **Greek Language Support**: Properly displays Greek text

## 🧪 Development

### Jupyter Notebook

The `greek-derby-rag.ipynb` notebook provides:
- Interactive development environment
- Step-by-step RAG system building
- Web scraping and data processing
- Vector store management
- Testing and debugging tools

### API Development

The FastAPI server includes:
- Automatic API documentation at `/docs`
- Interactive testing interface
- CORS support for web clients
- Error handling and validation
- Health monitoring

## 📊 Performance

### Memory Management
- **Conversation History**: Stored in memory during session
- **Vector Store**: Persistent storage in Pinecone
- **Export Functionality**: Save conversations to JSON files
- **Memory Clearing**: Reset conversation context

### Scalability
- **Stateless API**: Each request is independent
- **Vector Search**: Efficient semantic search
- **Caching**: Pinecone handles vector caching
- **Load Balancing**: FastAPI supports multiple workers

## 🛠️ Troubleshooting

### Common Issues

1. **API Keys Missing**:
   - Ensure `.env` file exists with valid keys
   - Check key permissions and quotas

2. **Pinecone Connection**:
   - Verify index name matches environment variable
   - Check Pinecone service status

3. **Web Client Issues**:
   - Ensure API server is running on port 8000
   - Check browser console for errors
   - Verify CORS settings

4. **Memory Issues**:
   - The chatbot creates a sample knowledge base if none exists
   - Check available RAM for large conversations

### Getting Help

1. Check the API documentation at `http://localhost:8000/docs`
2. Review the Jupyter notebook for implementation details
3. Check browser console for client-side errors
4. Verify all environment variables are set correctly

## 🔒 Security

### API Security
- **Input Validation**: All inputs are validated
- **Error Handling**: Sensitive information is not exposed
- **CORS Configuration**: Configurable for production use

### Data Privacy
- **No Data Storage**: Conversations are not permanently stored
- **API Key Protection**: Keys are loaded from environment variables
- **Local Processing**: All processing happens on your machine

## 📈 Future Enhancements

### Planned Features
- [ ] User authentication and profiles
- [ ] Conversation persistence in database
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Mobile app
- [ ] Real-time data updates

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational purposes. Please respect API usage limits and terms of service.

## 🙏 Acknowledgments

- **OpenAI** for language models and embeddings
- **Pinecone** for vector database services
- **LangChain** for RAG framework
- **FastAPI** for web framework
- **Greek Football Community** for inspiration

---

**🇬🇷 Enjoy chatting about the greatest derby in Greek football! ⚽**