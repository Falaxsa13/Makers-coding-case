from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.routes import inventory
from typing import List
from dotenv import load_dotenv
import os
from openai import OpenAI


# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# FastAPI app initialization
app = FastAPI()

# CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with specific origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# Base route for testing
@app.get("/")
def read_root():
    return {"message": "Welcome to the ChatBot Backend!"}

# Include API routes
app.include_router(inventory.router, prefix="/api/inventory", tags=["Inventory"])

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"User: {data}")

            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": data}
                    ],
                    temperature=0.7,
                    max_tokens=150
                )
                ai_message = response.choices[0].message.content

                await manager.broadcast(f"AI: {ai_message}")
            except Exception as e:
                error_message = f"Error generating response: {str(e)}"
                print(error_message)
                await websocket.send_text("AI: Sorry, there was an error generating a response.")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")
