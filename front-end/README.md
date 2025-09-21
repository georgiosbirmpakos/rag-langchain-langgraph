# 🇬🇷 Greek Derby Chatbot - React Frontend

A modern React application inspired by [Gazzetta.gr](https://www.gazzetta.gr/) design aesthetics, featuring a clean, professional sports website interface with contemporary React patterns and best practices.

## 🚀 Modern React Features Used

### 1. **React 19 with TypeScript**
- Latest React version with improved performance
- Full TypeScript support for type safety
- Vite for lightning-fast development

### 2. **Modern State Management**
- **useReducer + Context**: No external state management libraries needed
- **Custom Hooks**: Reusable logic for API calls and scroll behavior
- **Separation of Concerns**: Clean architecture with services, hooks, and components

### 3. **Component Architecture**
```
src/
├── components/          # Reusable UI components
│   ├── Chat.tsx        # Main chat orchestrator
│   ├── ChatInput.tsx   # Message input and sending
│   ├── Message.tsx     # Individual message display
│   ├── SampleQuestions.tsx # Clickable sample questions
│   └── Header.tsx      # Application header
├── hooks/              # Custom React hooks
│   ├── useApi.ts       # API calls with loading states
│   └── useScrollToBottom.ts # Scroll behavior logic
├── services/           # External API integration
│   └── api.ts         # Centralized API service
├── context/            # Global state management
│   └── ChatContext.tsx # Chat state and actions
└── types/              # TypeScript definitions
    └── index.ts        # All type definitions
```

## 🎯 Key Modern React Concepts Explained

### **1. Custom Hooks Pattern**
```typescript
// useApi.ts - Reusable API logic
export function useSendMessage() {
  const { data, loading, error, execute } = useApiCall<ChatResponse>();
  
  const sendMessage = useCallback(async (question: string) => {
    return execute(() => apiService.sendMessage(question));
  }, [execute]);
  
  return { response: data, loading, error, sendMessage };
}
```

**Why this is modern:**
- **Separation of Concerns**: API logic is separate from UI
- **Reusability**: Can be used in multiple components
- **Testability**: Easy to test in isolation
- **Type Safety**: Full TypeScript support

### **2. Context + useReducer Pattern**
```typescript
// ChatContext.tsx - Global state management
export function ChatProvider({ children }: ChatProviderProps) {
  const [state, dispatch] = useReducer(chatReducer, initialState);
  
  const addMessage = (text: string, sender: 'user' | 'bot', isError = false) => {
    const message: Message = { /* ... */ };
    dispatch({ type: 'ADD_MESSAGE', payload: message });
  };
  
  return (
    <ChatContext.Provider value={{ state, dispatch, addMessage, ... }}>
      {children}
    </ChatContext.Provider>
  );
}
```

**Why this is modern:**
- **No External Dependencies**: No Redux or Zustand needed
- **Predictable State Updates**: useReducer ensures consistent state changes
- **Performance**: Only re-renders when necessary
- **Developer Experience**: Clear action types and reducers

### **3. Service Layer Pattern**
```typescript
// api.ts - Centralized API calls
export const apiService = {
  async sendMessage(question: string): Promise<ChatResponse> {
    return apiRequest<ChatResponse>('/chat', {
      method: 'POST',
      body: JSON.stringify({ question }),
    });
  },
  // ... other API methods
};
```

**Why this is modern:**
- **Single Responsibility**: Each service handles one concern
- **Error Handling**: Centralized error management
- **Type Safety**: Full TypeScript integration
- **Maintainability**: Easy to modify API calls

### **4. Component Composition**
```typescript
// Chat.tsx - Main orchestrator component
export function Chat() {
  const { state } = useChat();
  const { scrollContainerRef, showScrollButton, scrollToBottom } = useScrollToBottom();
  
  return (
    <div className="chat-container">
      <div className="chat-messages" ref={scrollContainerRef}>
        {messages.map((message) => (
          <Message key={message.id} message={message} />
        ))}
      </div>
      <ChatInput />
      <SampleQuestions />
    </div>
  );
}
```

**Why this is modern:**
- **Composition over Inheritance**: Components work together
- **Single Responsibility**: Each component has one job
- **Reusability**: Components can be used elsewhere
- **Testability**: Easy to test individual components

## 🛠️ Development Commands

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linting
npm run lint
```

## 🎨 **Gazzetta.gr Inspired Design Features**

### ✅ **Modern Sports Website Aesthetics**
- **Clean, Professional Layout**: Card-based design with subtle shadows
- **Modern Color Palette**: Blues, whites, and subtle grays inspired by Gazzetta.gr
- **Professional Typography**: Inter font family for better readability
- **Gradient Backgrounds**: Subtle gradients for depth and visual interest
- **Smooth Animations**: Hover effects and transitions for better UX
- **Responsive Design**: Mobile-first approach that works on all devices

### ✅ **UI/UX Enhancements**
- **Card-based Messages**: Modern message bubbles with shadows and borders
- **Interactive Elements**: Hover effects and micro-animations
- **Loading States**: Animated loading indicators with pulse effects
- **Error Handling**: Clean error messages with appropriate styling
- **Scroll Button**: Modern floating action button with gradient styling
- **Sample Questions**: Clean button design with hover animations

### ✅ **Exact Feature Parity with Vanilla JS Version**
- Real-time chat interface
- Sample questions with click-to-send
- Auto-scroll to bottom
- Loading states and error handling
- Responsive design
- Greek language support

### ✅ **Modern React Enhancements**
- TypeScript for type safety
- Custom hooks for reusable logic
- Context for state management
- Service layer for API calls
- Component composition
- Error boundaries (implicit)

### ✅ **Performance Optimizations**
- useCallback for function memoization
- useReducer for efficient state updates
- Proper dependency arrays
- Minimal re-renders

## 🔧 How to Use

1. **Start the Backend API** (from project root):
   ```bash
   cd backend/api
   python greek_derby_api.py
   ```

2. **Start the React Frontend**:
   ```bash
   cd front-end/react-chatbot
   npm install
   npm run dev
   ```

3. **Open your browser** to `http://localhost:5173`

## 📚 Learning Points

This project demonstrates:

1. **Modern React Patterns**: Hooks, Context, Custom Hooks
2. **TypeScript Integration**: Type safety throughout
3. **Component Architecture**: Separation of concerns
4. **State Management**: Without external libraries
5. **API Integration**: Clean service layer
6. **Responsive Design**: Mobile-first approach
7. **Error Handling**: Comprehensive error management
8. **Performance**: Optimized re-renders

## 🎓 Next Steps for Learning

1. **Add Testing**: Jest + React Testing Library
2. **Add Routing**: React Router for multiple pages
3. **Add PWA Features**: Service workers, offline support
4. **Add State Persistence**: localStorage integration
5. **Add Animation**: Framer Motion for smooth transitions
6. **Add Accessibility**: ARIA labels, keyboard navigation

This React implementation showcases modern development practices while maintaining the exact same functionality as the vanilla JavaScript version!