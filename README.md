# Greek Derby RAG Chatbot 🇬🇷⚽

An interactive chatbot about the Olympiakos vs Panathinaikos derby using RAG (Retrieval-Augmented Generation) with memory.

## Features

- 🤖 **Interactive Chat**: Real-time conversation about the Greek derby
- 🧠 **Memory**: Remembers conversation history
- 📚 **RAG System**: Retrieves relevant information from knowledge base
- 🇬🇷 **Greek Language**: Fully supports Greek language
- 💾 **Export**: Save conversations to JSON files
- 📊 **Statistics**: View conversation analytics

## Quick Start

### 1. Setup

```bash
# Install dependencies
python setup.py

# Or manually install
pip install -r requirements.txt
```

### 2. Configure Environment

Edit the `.env` file with your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=your_index_name
```

### 3. Run the Chatbot

```bash
python greek_derby_chatbot.py
```

## Usage

### Interactive Commands

- Ask any question about the derby in Greek
- `ιστορικό` - Show conversation history
- `διαγραφή` - Clear memory
- `στατιστικά` - Show statistics
- `εξαγωγή` - Export conversation
- `βοήθεια` - Show help
- `έξοδος` - Exit

### Example Questions

- "Ποια είναι η ιστορία του ντέρμπι;"
- "Ποιος έχει κερδίσει περισσότερες φορές;"
- "Ποιοι είναι οι κορυφαίοι παίκτες;"
- "Ποια είναι τα πιο αξέχαστα γκολ;"
- "Που γίνεται το ντέρμπι;"

## Architecture

### Components

1. **Language Model**: GPT-4o-mini for Greek language support
2. **Embeddings**: OpenAI text-embedding-3-small for Greek text
3. **Vector Store**: Pinecone for document storage and retrieval
4. **RAG System**: LangGraph-based retrieval and generation
5. **Memory**: ConversationBufferMemory for context awareness

### Knowledge Base

The chatbot includes a comprehensive knowledge base about:
- Derby history and statistics
- Key players and moments
- Stadium information
- Fan culture and significance

## Files

- `greek_derby_chatbot.py` - Main chatbot application
- `requirements.txt` - Python dependencies
- `setup.py` - Setup script
- `README.md` - This documentation

## Requirements

- Python 3.8+
- OpenAI API key
- Pinecone API key
- Internet connection

## Troubleshooting

### Common Issues

1. **Missing API Keys**: Make sure your `.env` file has valid API keys
2. **Import Errors**: Run `pip install -r requirements.txt`
3. **Memory Issues**: The chatbot creates a sample knowledge base if none exists

### Getting Help

If you encounter issues:
1. Check your API keys are valid
2. Ensure all dependencies are installed
3. Verify internet connection
4. Check Pinecone index exists

## License

This project is for educational purposes. Please respect API usage limits and terms of service.

## Contributing

Feel free to submit issues and enhancement requests!
