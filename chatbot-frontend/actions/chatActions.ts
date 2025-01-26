'use server'

export const handleWebSockets = () => {
    const websocket = new WebSocket('ws://localhost:8000/ws/chat');
    websocket.onmessage = (event) => {
      console.log('Message received:', event.data);
      try {
        const message = JSON.parse(event.data);
        return message;
      } catch (error) {
        console.error('Error parsing message:', error);
      }
    };

}
