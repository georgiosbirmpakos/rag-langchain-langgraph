"""
Greek Derby RAG Chatbot
A standalone interactive chatbot about Olympiakos vs Panathinaikos derby
using RAG (Retrieval-Augmented Generation) with memory.
"""

import os
import sys
import json
from typing import List, Dict, Any
from datetime import datetime

# LangChain imports
from langchain.chat_models import init_chat_model
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict

# Web scraping imports
from langchain_community.document_loaders import WebBaseLoader

# Pinecone
from pinecone import Pinecone

class GreekDerbyState(TypedDict):
    question: str
    context: List[Document]
    answer: str

class GreekDerbyChatbot:
    """Interactive RAG chatbot for Greek Derby discussions"""
    
    def __init__(self):
        """Initialize the chatbot with all necessary components"""
        print("🚀 Initializing Greek Derby RAG Chatbot...")
        
        # Load environment variables
        self._load_environment()
        
        # Initialize components
        self._init_llm()
        self._init_embeddings()
        self._init_vector_store()
        self._init_rag_system()
        self._init_memory()
        
        # Load or create knowledge base
        self._load_knowledge_base()
        
        print("✅ Greek Derby Chatbot initialized successfully!")
    
    def _load_environment(self):
        """Load environment variables"""
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            print("⚠️  python-dotenv not installed. Make sure to set environment variables manually.")
        
        # Check required environment variables
        required_vars = ['OPENAI_API_KEY', 'PINECONE_API_KEY', 'PINECONE_GREEK_DERBY_INDEX_NAME']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
            print("Please set these variables in your .env file or environment")
            sys.exit(1)
        
        print("✅ Environment variables loaded")
    
    def _init_llm(self):
        """Initialize the language model"""
        self.llm = init_chat_model("gpt-4o-mini", model_provider="openai")
        print("✅ Language model initialized")
    
    def _init_embeddings(self):
        """Initialize embeddings model"""
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            dimensions=1024
        )
        print("✅ Embeddings model initialized")
    
    def _init_vector_store(self):
        """Initialize vector store"""
        pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
        self.index = pc.Index(os.getenv('PINECONE_INDEX_NAME'))
        self.vector_store = PineconeVectorStore(embedding=self.embeddings, index=self.index)
        print("✅ Vector store initialized")
    
    def _init_rag_system(self):
        """Initialize RAG system components"""
        # Create Greek language prompt
        self.prompt = PromptTemplate(
            input_variables=["question", "context"],
            template="""
Είστε ένας εξειδικευμένος βοηθός για το ελληνικό ποδόσφαιρο και το ντέρμπι Ολυμπιακός-Παναθηναϊκός.

Χρησιμοποιήστε τις παρακάτω πληροφορίες για να απαντήσετε στην ερώτηση του χρήστη.
Αν δεν γνωρίζετε την απάντηση, πείτε ότι δεν γνωρίζετε.
Απαντήστε στα ελληνικά με φιλικό και ενημερωτικό τρόπο.
Κρατήστε τις απαντήσεις συνοπτικές αλλά πλήρεις.

Περιεχόμενο: {context}

Ερώτηση: {question}
Απάντηση:"""
        )
        
        # Define RAG functions
        def retrieve_greek_content(state: GreekDerbyState):
            retrieved_docs = self.vector_store.similarity_search(
                state["question"], 
                k=4
            )
            return {"context": retrieved_docs}

        def generate_greek_answer(state: GreekDerbyState):
            docs_content = "\n\n".join([doc.page_content for doc in state["context"]])
            messages = self.prompt.invoke({"question": state["question"], "context": docs_content})
            response = self.llm.invoke(messages)
            return {"answer": response.content}
        
        # Build RAG graph
        graph_builder = StateGraph(GreekDerbyState)
        graph_builder.add_sequence([retrieve_greek_content, generate_greek_answer])
        graph_builder.add_edge(START, "retrieve_greek_content")
        self.rag_graph = graph_builder.compile()
        
        print("✅ RAG system initialized")
    
    def _init_memory(self):
        """Initialize conversation memory"""
        self.memory = ConversationBufferMemory(return_messages=True)
        self.conversation_history = []
        
        # Enhanced prompt for conversational RAG
        self.chat_prompt = ChatPromptTemplate.from_messages([
            ("system", """Είστε ένας εξειδικευμένος βοηθός για το ελληνικό ποδόσφαιρο και το ντέρμπι Ολυμπιακός-Παναθηναϊκός.

Χρησιμοποιήστε τις παρακάτω πληροφορίες για να απαντήσετε στην ερώτηση του χρήστη.
Αν δεν γνωρίζετε την απάντηση, πείτε ότι δεν γνωρίζετε.
Απαντήστε στα ελληνικά με φιλικό και ενημερωτικό τρόπο.
Κρατήστε τις απαντήσεις συνοπτικές αλλά πλήρεις.

Περιεχόμενο: {context}

Προηγούμενη συνομιλία:
{chat_history}

Ερώτηση: {question}
Απάντηση:"""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}")
        ])
        
        print("✅ Memory system initialized")
    
    def _load_knowledge_base(self):
        """Load or create the knowledge base"""
        stats = self.index.describe_index_stats()
        
        if stats['total_vector_count'] == 0:
            print("📚 No knowledge base found. Creating sample content...")
            self._create_sample_knowledge_base()
        else:
            print(f"📚 Knowledge base loaded with {stats['total_vector_count']} vectors")
    
    def _create_sample_knowledge_base(self):
        """Create sample knowledge base with Greek derby content"""
        sample_content = """
Ολυμπιακός vs Παναθηναϊκός - Το Μεγάλο Ντέρμπι της Ελλάδας

Το ντέρμπι μεταξύ Ολυμπιακού και Παναθηναϊκού είναι το πιο σημαντικό ποδοσφαιρικό γεγονός στην Ελλάδα. 
Αυτό το ματς, γνωστό ως "Το Μεγάλο Ντέρμπι", συγκεντρώνει εκατομμύρια θεατές και φιλάθλους.

Ιστορία του Ντέρμπι:
Το πρώτο επίσημο ματς μεταξύ των δύο ομάδων έγινε το 1925. Από τότε, έχουν αγωνιστεί 
εκατοντάδες φορές, με κάθε ματς να είναι γεμάτο πάθος και συναίσθημα.

Σημαντικές Στιγμές:
- Το 2004, ο Ολυμπιακός κέρδισε 3-1 στο ΟΑΚΑ
- Το 2007, ο Παναθηναϊκός επικράτησε 2-1 στο Καραϊσκάκη
- Το 2010, ισόπαλος 1-1 με αξέχαστα γκολ

Κορυφαίοι Παίκτες:
- Γιώργος Καραγκούνης (Παναθηναϊκός)
- Γιώργος Σεϊταρίδης (Ολυμπιακός)
- Αντώνης Νικοπολίδης (Ολυμπιακός)
- Αντώνης Αντωνιάδης (Παναθηναϊκός)

Σημασία για τους Φιλάθλους:
Το ντέρμπι δεν είναι απλά ένα ποδοσφαιρικό ματς, αλλά μια σύγκρουση ταυτοτήτων, 
ιστοριών και παθών. Κάθε φίλαθλος περιμένει με αγωνία αυτό το ματς όλο το χρόνο.

Γήπεδα:
- Ολυμπιακός: Γεώργιος Καραϊσκάκης (Πειραιάς)
- Παναθηναϊκός: Απόστολος Νικολαΐδης (Αθήνα)

Στατιστικά:
Ο Ολυμπιακός έχει κερδίσει περισσότερες φορές το ντέρμπι στην ιστορία.
Οι αγώνες είναι γεμάτοι ένταση και συχνά κρίνουν τίτλους.
        """
        
        # Create document
        sample_doc = Document(
            page_content=sample_content,
            metadata={"source": "sample_content", "type": "greek_derby_info"}
        )
        
        # Split and store
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""]
        )
        
        splits = text_splitter.split_documents([sample_doc])
        self.vector_store.add_documents(splits)
        
        print(f"✅ Sample knowledge base created with {len(splits)} chunks")
    
    def chat(self, user_input: str) -> str:
        """Process user input and return chatbot response"""
        try:
            # Get relevant context using RAG
            rag_response = self.rag_graph.invoke({"question": user_input})
            context = rag_response.get("context", [])
            
            # Format context for the prompt
            context_text = "\n\n".join([doc.page_content for doc in context])
            
            # Get conversation history
            chat_history = self.memory.chat_memory.messages
            
            # Create the prompt
            messages = self.chat_prompt.format_messages(
                context=context_text,
                chat_history=chat_history,
                question=user_input
            )
            
            # Get response from LLM
            response = self.llm.invoke(messages)
            
            # Store in memory
            self.memory.chat_memory.add_user_message(user_input)
            self.memory.chat_memory.add_ai_message(response.content)
            
            # Store in conversation history
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "user": user_input,
                "bot": response.content,
                "context_sources": [doc.metadata.get("source", "unknown") for doc in context]
            })
            
            return response.content
            
        except Exception as e:
            error_msg = f"Σφάλμα: {str(e)}"
            self.memory.chat_memory.add_user_message(user_input)
            self.memory.chat_memory.add_ai_message(error_msg)
            return error_msg
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the full conversation history"""
        return self.conversation_history
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.memory.clear()
        self.conversation_history = []
        print("Η μνήμη της συνομιλίας διαγράφηκε.")
    
    def get_memory_summary(self) -> str:
        """Get a summary of the conversation"""
        if not self.conversation_history:
            return "Δεν υπάρχει ιστορικό συνομιλίας."
        
        summary = f"Συνομιλία με {len(self.conversation_history)} ερωτήσεις:\n"
        for i, conv in enumerate(self.conversation_history, 1):
            summary += f"{i}. Ερώτηση: {conv['user'][:50]}...\n"
            summary += f"   Απάντηση: {conv['bot'][:50]}...\n"
        
        return summary
    
    def export_conversation(self, filename: str = None):
        """Export conversation to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"greek_derby_chat_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
        print(f"Συνομιλία εξήχθη στο αρχείο: {filename}")
    
    def get_stats(self) -> str:
        """Get conversation statistics"""
        if not self.conversation_history:
            return "Δεν υπάρχει συνομιλία ακόμα."
        
        total_questions = len(self.conversation_history)
        total_chars = sum(len(conv['user']) + len(conv['bot']) for conv in self.conversation_history)
        avg_question_length = sum(len(conv['user']) for conv in self.conversation_history) / total_questions
        avg_answer_length = sum(len(conv['bot']) for conv in self.conversation_history) / total_questions
        
        return f"""
📊 Στατιστικά Συνομιλίας:
- Συνολικές Ερωτήσεις: {total_questions}
- Συνολικοί Χαρακτήρες: {total_chars:,}
- Μέσος Όρος Μήκους Ερώτησης: {avg_question_length:.1f} χαρακτήρες
- Μέσος Όρος Μήκους Απάντησης: {avg_answer_length:.1f} χαρακτήρες
"""

def print_welcome():
    """Print welcome message"""
    print("=" * 70)
    print("🇬🇷 GREEK DERBY RAG CHATBOT 🇬🇷")
    print("=" * 70)
    print("Καλώς ήρθατε στο chatbot για το ντέρμπι Ολυμπιακός-Παναθηναϊκός!")
    print("Μπορείτε να ρωτήσετε οτιδήποτε σχετικά με το μεγάλο ντέρμπι.")
    print("=" * 70)
    print("Εντολές:")
    print("  - Ρωτήστε οτιδήποτε για το ντέρμπι")
    print("  - 'ιστορικό' - Δείτε το ιστορικό συνομιλίας")
    print("  - 'διαγραφή' - Διαγράψτε τη μνήμη")
    print("  - 'στατιστικά' - Δείτε στατιστικά")
    print("  - 'εξαγωγή' - Εξάγετε τη συνομιλία")
    print("  - 'βοήθεια' - Δείτε αυτές τις εντολές")
    print("  - 'έξοδος' - Τερματίστε το πρόγραμμα")
    print("=" * 70)

def main():
    """Main function to run the chatbot"""
    try:
        # Initialize chatbot
        chatbot = GreekDerbyChatbot()
        
        # Print welcome message
        print_welcome()
        
        # Main chat loop
        while True:
            try:
                # Get user input
                user_input = input("\n👤 Εσείς: ").strip()
                
                # Handle special commands
                if user_input.lower() in ['έξοδος', 'exit', 'quit', 'q']:
                    print("\n👋 Αντίο! Ευχαριστούμε που συνομλήσατε για το ντέρμπι!")
                    break
                elif user_input.lower() == 'ιστορικό':
                    print("\n📚 Ιστορικό Συνομιλίας:")
                    print(chatbot.get_memory_summary())
                    continue
                elif user_input.lower() == 'διαγραφή':
                    chatbot.clear_memory()
                    continue
                elif user_input.lower() == 'στατιστικά':
                    print(chatbot.get_stats())
                    continue
                elif user_input.lower() == 'εξαγωγή':
                    chatbot.export_conversation()
                    continue
                elif user_input.lower() == 'βοήθεια':
                    print_welcome()
                    continue
                elif not user_input:
                    print("Παρακαλώ εισάγετε μια ερώτηση ή εντολή.")
                    continue
                
                # Get chatbot response
                print("\n🤖 Bot: ", end="")
                response = chatbot.chat(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Αντίο! Ευχαριστούμε που συνομλήσατε για το ντέρμπι!")
                break
            except Exception as e:
                print(f"\n❌ Σφάλμα: {e}")
                print("Παρακαλώ δοκιμάστε ξανά ή πληκτρολογήστε 'έξοδος' για να τερματίσετε.")
    
    except Exception as e:
        print(f"❌ Κρίσιμο σφάλμα κατά την αρχικοποίηση: {e}")
        print("Παρακαλώ ελέγξτε τις μεταβλητές περιβάλλοντος και τις συνδέσεις.")
        sys.exit(1)

if __name__ == "__main__":
    main()
