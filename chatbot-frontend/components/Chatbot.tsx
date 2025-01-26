'use client';
import { useEffect, useRef, useState } from 'react';
import { Input } from './ui/input';
import { useWebSocket } from '@/provider/WebSockerProvider';
import { Button } from './ui/button';

interface ChatMessage {
  user: 'IA' | 'client';
  message: string;
}

const Chatbot: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState<string>('');
  const { ws, sendMessage: sendWebSocketMessage } = useWebSocket();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!ws) return;

    ws.onmessage = (event) => {
      console.log('Received message event:', event);
      const message: ChatMessage = { user: 'IA', message: event.data };
      setMessages((prevMessages) => [...prevMessages, message]);
    };

    return () => {
      ws.onmessage = null;
    };
  }, [ws]);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);


  const sendMessage = () => {
    if (input.trim()) {
      console.log('Sending message:', input);
      const message: ChatMessage = { user: 'client', message: input };
      setMessages((prevMessages) => [...prevMessages, message]);
      sendWebSocketMessage(input);
      setInput('');
    }
  };

  console.log('Current messages:', messages);

  return (
    <div className="chatbot-container border border-primary h-[800px] p-4 flex flex-col justify-between">
      <div className="messages space-y-2 flex-1 overflow-auto">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`message p-2 px-4 rounded-md max-w-xs w-fit border ${
              message.user === 'IA' ? 'bg-background text-left' : 'bg-primary text-background text-right ml-auto'
            }`}
          >
            {message.user === 'IA' ? message.message : `You: ${message.message}`}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="flex mt-4">
        <Input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => (e.key === 'Enter' ? sendMessage() : null)}
          className=" p-2 border border-gray-300 rounded-l-md"
        />
        <Button onClick={sendMessage}>
          Send
        </Button>
      </div>
    </div>
  );
};

export default Chatbot;
