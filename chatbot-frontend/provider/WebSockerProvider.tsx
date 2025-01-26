"use client";
import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";

// Define la interfaz para el valor del contexto de WebSocket
interface WebSocketContextValue {
  ws: WebSocket | null;
  sendMessage: (message: string) => void;
}

// Crea el contexto de WebSocket con un valor inicial indefinido
const WebSocketContext = createContext<WebSocketContextValue | undefined>(
  undefined,
);

// Hook personalizado para usar el contexto de WebSocket
export const useWebSocket = () => {
  const context = useContext(WebSocketContext);
  if (!context) {
    throw new Error("useWebSocket must be used within a WebSocketProvider");
  }
  return context;
};

// Define las propiedades para el proveedor de WebSocket
interface WebSocketProviderProps {
  children: ReactNode;
}

// Componente proveedor de WebSocket
export const WebSocketProvider: React.FC<WebSocketProviderProps> = ({
  children,
}) => {
  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    console.log("useEffect called - Connecting to WebSocket...");
    // Crea una nueva conexión WebSocket
    const websocket = new WebSocket("ws://localhost:8000/ws/chat");

    // Evento cuando la conexión se abre
    websocket.onopen = () => {
      console.log("Connected to WebSocket");
    };

    // Evento cuando ocurre un error en la conexión
    websocket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    // Evento cuando la conexión se cierra
    websocket.onclose = () => {
      console.log("Disconnected from WebSocket");
    };

    // Establece el WebSocket en el estado
    setWs(websocket);

    // Limpia la conexión WebSocket cuando el componente se desmonta
    return () => {
      console.log("Closing WebSocket connection...");
      websocket.close();
    };
  }, []);

  // Función para enviar un mensaje a través del WebSocket
  const sendMessage = (message: string) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      console.log("Sending message:", message);
      ws.send(message);
    }
  };

  // Proporciona el contexto de WebSocket a los componentes hijos
  return (
    <WebSocketContext.Provider value={{ ws, sendMessage }}>
      {children}
    </WebSocketContext.Provider>
  );
};
