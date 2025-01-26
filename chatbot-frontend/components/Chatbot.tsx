"use client";
import { useEffect, useRef, useState } from "react";
import { Input } from "./ui/input";
import { useWebSocket } from "@/provider/WebSockerProvider";
import { Button } from "./ui/button";

// Define la interfaz para los mensajes del chat
interface ChatMessage {
  user: "IA" | "client";
  message: string;
}

const Chatbot: React.FC = () => {
  // Estado para almacenar los mensajes del chat
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  // Estado para almacenar el valor del input
  const [input, setInput] = useState<string>("");
  // Obtiene el WebSocket y la función sendMessage del contexto
  const { ws, sendMessage: sendWebSocketMessage } = useWebSocket();
  // Referencia al final de la lista de mensajes para el scroll automático
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // useEffect para manejar la recepción de mensajes del WebSocket
  useEffect(() => {
    if (!ws) return;

    // Evento cuando se recibe un mensaje del WebSocket
    ws.onmessage = (event) => {
      console.log("Received message event:", event);
      const message: ChatMessage = { user: "IA", message: event.data };
      setMessages((prevMessages) => [...prevMessages, message]);
    };

    // Limpia el evento onmessage cuando el componente se desmonta
    return () => {
      ws.onmessage = null;
    };
  }, [ws]);

  // useEffect para hacer scroll automático al final de la lista de mensajes
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  // Función para enviar un mensaje
  const sendMessage = () => {
    if (input.trim()) {
      console.log("Sending message:", input);
      const message: ChatMessage = { user: "client", message: input };
      setMessages((prevMessages) => [...prevMessages, message]);
      sendWebSocketMessage(input);
      setInput("");
    }
  };

  console.log("Current messages:", messages);

  return (
    <div className="chatbot-container border border-primary h-[800px] p-4 flex flex-col justify-between">
      <div className="messages space-y-2 flex-1 overflow-auto">
        {/* Renderiza los mensajes aquí */}
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.user}`}>
            {msg.message}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="input-container flex">
        <Input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => (e.key === "Enter" ? sendMessage() : null)}
          className="flex-1"
        />
        <Button onClick={sendMessage}>Send</Button>
      </div>
    </div>
  );
};

export default Chatbot;
