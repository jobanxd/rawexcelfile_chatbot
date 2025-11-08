import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(() => generateSessionId());
  const [animatingMessage, setAnimatingMessage] = useState(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Generate a unique session ID
  function generateSessionId() {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, animatingMessage]);

  // Handle New Chat button
  const handleNewChat = () => {
    setMessages([]);
    setSessionId(generateSessionId());
    setInputMessage('');
    setAnimatingMessage(null);
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    
    if (!inputMessage.trim()) return;

    const userMessageContent = inputMessage;
    
    // Create user message for animation
    const userMessage = {
      role: 'user',
      content: userMessageContent
    };

    // Show the message animating from input box
    setAnimatingMessage(userMessage);
    setInputMessage('');
    
    // Wait for animation to complete before adding to messages
    setTimeout(() => {
      setMessages(prev => [...prev, userMessage]);
      setAnimatingMessage(null);
      setIsLoading(true);
    }, 500);

    try {
      // Call your backend API with dynamic session_id
      const response = await axios.post('http://localhost:8000/api/generate', {
        session_id: sessionId,
        user_id: 'user_001',
        input_query: userMessageContent
      });

      // Add bot response to chat
      const botMessage = {
        role: 'assistant',
        content: response.data.response
      };
      
      setTimeout(() => {
        setMessages(prev => [...prev, botMessage]);
        setIsLoading(false);
      }, 500);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, something went wrong. Please try again.'
      };
      setMessages(prev => [...prev, errorMessage]);
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header with glassmorphism */}
      <div className="backdrop-blur-xl bg-white/10 border-b border-white/20 px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-semibold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
          AI Chatbot
        </h1>
        <div className="flex items-center gap-4">
          <span className="text-sm text-gray-300">
            Session: <span className="font-mono text-purple-300">{sessionId}</span>
          </span>
          <button
            onClick={handleNewChat}
            className="px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all duration-300 font-medium shadow-lg shadow-purple-500/50"
          >
            + New Chat
          </button>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-3xl mx-auto space-y-6">
          {messages.length === 0 && !animatingMessage && (
            <div className="text-center text-gray-300 mt-20">
              <div className="text-6xl mb-4">✨</div>
              <p className="text-2xl font-light bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                How can I help you today?
              </p>
            </div>
          )}
          
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} animate-slide-up`}
            >
              <div
                className={`max-w-[80%] rounded-2xl px-5 py-4 shadow-lg ${
                  message.role === 'user'
                    ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white'
                    : 'backdrop-blur-xl bg-white/10 text-gray-100 border border-white/20'
                }`}
              >
                {message.role === 'user' ? (
                  <p className="whitespace-pre-wrap">{message.content}</p>
                ) : (
                  <ReactMarkdown>{message.content}</ReactMarkdown>
                )}
              </div>
            </div>
          ))}

          {/* Animating message from input */}
          {animatingMessage && (
            <div className="flex justify-end">
              <div className="max-w-[80%] rounded-2xl px-5 py-4 shadow-lg bg-gradient-to-r from-blue-500 to-purple-500 text-white animate-bubble-up">
                <p className="whitespace-pre-wrap">{animatingMessage.content}</p>
              </div>
            </div>
          )}
          
          {/* Thinking indicator */}
          {isLoading && (
            <div className="flex justify-start animate-slide-up">
              <div className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-2xl px-5 py-4 shadow-lg">
                <div className="flex items-center gap-3">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                    <div className="w-2 h-2 bg-pink-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                  </div>
                  <span className="text-gray-300 animate-pulse">Thinking</span>
                  <span className="text-gray-300 animate-ellipsis">...</span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area with glassmorphism */}
      <div className="backdrop-blur-xl bg-white/10 border-t border-white/20 px-4 py-4">
        <div className="max-w-3xl mx-auto">
          <form onSubmit={sendMessage} className="flex gap-3">
            <input
              ref={inputRef}
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Type your message..."
              className="flex-1 px-5 py-3 bg-white/10 backdrop-blur-xl border border-white/20 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent text-white placeholder-gray-400 transition-all"
              disabled={isLoading || animatingMessage}
            />
            <button
              type="submit"
              disabled={isLoading || !inputMessage.trim() || animatingMessage}
              className="px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl hover:from-purple-600 hover:to-pink-600 disabled:from-gray-600 disabled:to-gray-600 disabled:cursor-not-allowed transition-all duration-300 font-medium shadow-lg shadow-purple-500/50 hover:shadow-purple-500/70"
            >
              Send
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default App;