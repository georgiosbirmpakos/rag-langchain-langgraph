# Greek Derby RAG Chatbot 🇬🇷⚽

A comprehensive RAG (Retrieval-Augmented Generation) chatbot system about the Olympiakos vs Panathinaikos derby, featuring real-time content from [Gazzetta.gr](https://www.gazzetta.gr/), multiple frontend interfaces, and a robust backend API.

## 🌟 Features

### **🤖 Advanced RAG System**
- **Real-time Content**: Automatically fetches latest news from Gazzetta.gr
- **Intelligent Retrieval**: LangGraph-based RAG with semantic search
- **Memory System**: Conversation history and context awareness
- **Greek Language**: Full support for Greek language with proper prompts

### **🎨 Multiple Frontend Options**
- **React Frontend**: Modern, responsive React application with Gazzetta.gr-inspired design
- **Vanilla JavaScript**: Lightweight HTML/CSS/JS client
- **Web API**: FastAPI-based REST API with automatic documentation
- **Jupyter Notebook**: Interactive development and testing environment

### **📚 Knowledge Base**
- **Gazzetta.gr Integration**: Live content from Greece's premier sports website
- **Multi-source Data**: Olympiakos, Panathinaikos, and Super League pages
- **Intelligent Fallback**: Sample content if web scraping fails
- **Vector Storage**: Pinecone for efficient semantic search

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8+
- npm (for React frontend dependencies)
- OpenAI API key
- Pinecone API key

### **1. Clone and Setup**
```bash
git clone <repository-url>
cd rag-langchain-langgraph
```

### **2. Environment Configuration**
Create a `.env` file in the project root:
```env
# Required API Keys
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_GREEK_DERBY_INDEX_NAME=your_index_name

# Optional
USER_AGENT=greek-derby-chatbot/1.0
```

### **3. Install Dependencies**

**Backend Dependencies:**
```bash
pip install -r requirements_api.txt
```

**Frontend Dependencies:**
```bash
cd front-end/react-chatbot
npm install
```

### **4. Start the Application**

**Option A: Full Stack (Recommended)**
```bash
# Terminal 1: Start Backend API
cd backend/api
python greek_derby_api.py

# Terminal 2: Start React Frontend
cd front-end/react-chatbot
npm run dev
```

**Option B: Vanilla JavaScript Frontend**
```bash
# Terminal 1: Start Backend API
cd backend/api
python greek_derby_api.py

# Terminal 2: Open HTML client
# Open front-end/vanilla_javascript/chatbot_web_client.html in browser
```

**Option C: Standalone Application**
```bash
cd backend/standalone-service
python greek_derby_chatbot.py
```

## 📁 Project Structure

```
rag-langchain-langgraph/
├── backend/
│   ├── api/
│   │   └── greek_derby_api.py          # FastAPI web server
│   ├── standalone-service/
│   │   └── greek_derby_chatbot.py      # Core RAG chatbot
│   └── README.md                       # Backend documentation
├── front-end/
│   ├── react-chatbot/                  # Modern React frontend
│   │   ├── src/
│   │   │   ├── components/             # React components
│   │   │   ├── hooks/                  # Custom React hooks
│   │   │   ├── services/               # API service layer
│   │   │   ├── context/                # State management
│   │   │   └── types/                  # TypeScript definitions
│   │   ├── package.json
│   │   └── README.md
│   └── vanilla_javascript/
│       └── chatbot_web_client.html     # Lightweight HTML client
├── ipynb testing/
│   ├── greek-derby-rag.ipynb           # Development notebook
│   └── rag-langchain-langgraph.ipynb   # RAG tutorial notebook
├── requirements_api.txt                # Python dependencies
├── .env                               # Environment variables (create this)
└── README.md                          # This file
```

## 🎨 Frontend Options

### **React Frontend (Modern)**
- **Framework**: React 19 with TypeScript
- **Styling**: Gazzetta.gr-inspired design with modern CSS
- **State Management**: Context API with useReducer
- **API Integration**: Custom hooks for API calls
- **Features**: Responsive design, smooth animations, error handling

**Start React Frontend:**
```bash
cd front-end/react-chatbot
npm install
npm run dev
# Open http://localhost:5173
```

### **Vanilla JavaScript Frontend (Lightweight)**
- **Technology**: Pure HTML/CSS/JavaScript
- **Features**: Fullscreen interface, real-time chat, sample questions
- **Compatibility**: Works in any modern browser

**Use Vanilla Frontend:**
```bash
# Start backend first
cd backend/api
python greek_derby_api.py

# Open in browser
# front-end/vanilla_javascript/chatbot_web_client.html
```

## 🌐 Backend API

### **Core Endpoints**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information and sample questions |
| `GET` | `/health` | Health check and system status |
| `POST` | `/chat` | Send message to chatbot |
| `GET` | `/history` | Get conversation history |
| `GET` | `/stats` | Get conversation statistics |
| `POST` | `/clear` | Clear conversation memory |
| `GET` | `/export` | Export conversation to JSON |
| `GET` | `/sample-questions` | Get sample questions |

### **API Documentation**
- **Interactive Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

### **Example API Usage**
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

## 🔄 Gazzetta.gr Integration

### **Content Sources**
The system automatically loads content from:
- **Olympiakos Page**: `https://www.gazzetta.gr/football/superleague/olympiakos`
- **Panathinaikos Page**: `https://www.gazzetta.gr/football/superleague/panathinaikos`
- **Super League Page**: `https://www.gazzetta.gr/football/superleague`
- **Main Gazzetta Page**: `https://www.gazzetta.gr`

### **Content Processing**
- **Smart Scraping**: Multiple CSS selectors for optimal content extraction
- **Fallback Methods**: Alternative approaches if primary scraping fails
- **Content Filtering**: Removes irrelevant or short content
- **Greek-friendly Splitting**: Optimized chunking for Greek language
- **Metadata Enrichment**: Source URLs and content type information

## 🧠 RAG System Architecture

### **Core Components**
1. **Language Model**: GPT-4o-mini for Greek language support
2. **Embeddings**: OpenAI text-embedding-3-small (1024 dimensions)
3. **Vector Store**: Pinecone for document storage and retrieval
4. **RAG Pipeline**: LangGraph-based retrieval and generation
5. **Memory**: ConversationBufferMemory for context awareness
6. **Web Framework**: FastAPI for REST API
7. **Frontend**: React/HTML clients for user interaction

### **Knowledge Base**
- **Real-time Content**: Live data from Gazzetta.gr
- **Historical Data**: Sample content as fallback
- **Vector Search**: Semantic similarity search
- **Chunk Management**: 500-character chunks with 100-character overlap

## 💻 Usage Examples

### **Sample Questions**
- "Ποια είναι η ιστορία του ντέρμπι;"
- "Ποιος έχει κερδίσει περισσότερες φορές;"
- "Ποιοι είναι οι κορυφαίοι παίκτες;"
- "Ποια είναι τα πιο αξέχαστα γκολ;"
- "Που γίνεται το ντέρμπι;"
- "Ποια είναι η σημασία για τους φιλάθλους;"
- "Ποια είναι τα στατιστικά;"
- "Ποια είναι τα γήπεδα;"

### **Interactive Commands (Standalone App)**
- Ask any question about the derby in Greek
- `ιστορικό` - Show conversation history
- `διαγραφή` - Clear memory
- `στατιστικά` - Show statistics
- `εξαγωγή` - Export conversation
- `βοήθεια` - Show help
- `έξοδος` - Exit

## 🔧 Configuration

### **Environment Variables**
```env
# Required
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_GREEK_DERBY_INDEX_NAME=your_index_name

# Optional
USER_AGENT=greek-derby-chatbot/1.0
```

### **Pinecone Setup**
1. Create account at [pinecone.io](https://pinecone.io)
2. Create index with:
   - Dimensions: 1024 (for text-embedding-3-small)
   - Metric: cosine
   - Name: `greek-derby-index` (or your preferred name)

## 🎨 Design Features

### **React Frontend (Gazzetta.gr Inspired)**
- **Modern UI**: Clean, professional sports website aesthetic
- **Card-based Design**: Messages and components use card layouts
- **Gradient Backgrounds**: Professional blue gradients
- **Smooth Animations**: Hover effects and transitions
- **Responsive Design**: Works on all devices
- **Greek Typography**: Inter font for better readability

### **Vanilla JavaScript Frontend**
- **Fullscreen Interface**: Immersive chat experience
- **Real-time Updates**: Instant message display
- **Sample Questions**: Click-to-send functionality
- **Scroll Controls**: Auto-scroll and manual controls
- **Error Handling**: Graceful error display

## 🧪 Development

### **Jupyter Notebooks**
- **greek-derby-rag.ipynb**: Complete RAG system implementation
- **rag-langchain-langgraph.ipynb**: RAG tutorial and development

### **API Development**
- **FastAPI**: Automatic documentation and testing
- **CORS Support**: Frontend integration ready
- **Error Handling**: Comprehensive error management
- **Health Monitoring**: System status endpoints

## 📊 Performance

### **Expected Performance**
- **Initial Load**: 30-60 seconds (Gazzetta.gr content loading)
- **Query Response**: 2-5 seconds per question
- **Memory Usage**: ~200-500MB depending on content size
- **Vector Storage**: ~1-5MB for typical content

### **Optimization Features**
- **Vector Caching**: Pinecone handles vector caching
- **Chunk Optimization**: Greek-friendly text splitting
- **Memory Management**: Efficient conversation storage
- **Error Recovery**: Graceful fallback mechanisms

## 🛠️ Troubleshooting

### **Common Issues**

1. **API Keys Missing**:
   - Ensure `.env` file exists with valid keys
   - Check key permissions and quotas

2. **Pinecone Connection**:
   - Verify index name matches environment variable
   - Check Pinecone service status

3. **Frontend Issues**:
   - Ensure backend API is running on port 8000
   - Check browser console for errors
   - Verify CORS settings

4. **Content Loading**:
   - System falls back to sample content if Gazzetta.gr fails
   - Check network connectivity
   - Verify USER_AGENT environment variable

### **Getting Help**
1. Check API documentation at `http://localhost:8000/docs`
2. Review Jupyter notebooks for implementation details
3. Check browser console for client-side errors
4. Verify all environment variables are set correctly

## 🔒 Security

### **API Security**
- **Input Validation**: Pydantic models for request validation
- **Error Handling**: No sensitive information exposure
- **CORS Configuration**: Configurable for production use

### **Data Privacy**
- **No Personal Data**: System doesn't store personal information
- **Local Processing**: All processing happens on your machine
- **API Key Protection**: Keys loaded from environment variables

## 📈 Future Enhancements

### **Planned Features**
- [ ] User authentication and profiles
- [ ] Conversation persistence in database
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Mobile app
- [ ] Real-time data updates
- [ ] Additional Greek sports websites

### **Contributing**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📚 Documentation

- **Backend**: `backend/README.md` - Detailed backend documentation
- **React Frontend**: `front-end/react-chatbot/README.md` - React-specific guide
- **API Docs**: `http://localhost:8000/docs` - Interactive API documentation