import React, { useState } from 'react';
import { Send, User, Bot, BookOpen } from 'lucide-react';
import { chatService } from '../services/api';

export default function ChatTab({ documentId }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || !documentId) return;

    const userMessage = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await chatService.askQuestion(documentId, userMessage.content);
      const botMessage = { 
        role: 'bot', 
        content: response.data.answer,
        sources: response.data.sources 
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      setMessages((prev) => [...prev, { role: 'bot', content: "Sorry, I encountered an error answering that." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[500px] bg-white rounded-lg border border-gray-200 shadow-sm">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-10">Ask a question about your document!</div>
        )}
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            {msg.role === 'bot' && <div className="w-8 h-8 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center shrink-0"><Bot size={18} /></div>}
            
            <div className={`max-w-[80%] rounded-lg p-3 ${msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-800'}`}>
              <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
              
              {/* Render Citations if available */}
              {msg.sources && msg.sources.length > 0 && (
                <div className="mt-3 pt-3 border-t border-gray-200">
                  <p className="text-xs font-semibold text-gray-500 flex items-center gap-1 mb-1">
                    <BookOpen size={12} /> Sources:
                  </p>
                  <ul className="space-y-1">
                    {msg.sources.map((src, i) => (
                      <li key={i} className="text-xs text-gray-500 bg-white p-1 rounded border border-gray-200 truncate">
                        Pg {src.page_number} ({src.filename}): "{src.content}"
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {msg.role === 'user' && <div className="w-8 h-8 bg-gray-200 text-gray-600 rounded-full flex items-center justify-center shrink-0"><User size={18} /></div>}
          </div>
        ))}
        {loading && <div className="text-gray-400 text-sm flex gap-2"><Bot size={18}/> Thinking...</div>}
      </div>

      <form onSubmit={handleSend} className="p-4 border-t border-gray-200 flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something..."
          className="flex-1 border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
          disabled={loading}
        />
        <button type="submit" disabled={loading} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50">
          <Send size={18} />
        </button>
      </form>
    </div>
  );
}