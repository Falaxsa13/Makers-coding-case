from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.routes import inventory
from typing import List
from dotenv import load_dotenv
import os
from openai import OpenAI
from utils.inventory import load_inventory, filter_by_category, find_item_by_name


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

from utils.inventory import load_inventory, filter_by_category, find_item_by_name

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        context = [{"role": "system", "content": "You are a helpful assistant who manages an inventory system."}]
        inventory = load_inventory()

        while True:
            user_message = await websocket.receive_text()
            print(f"User: {user_message}")

            # Add the user message to the context
            context.append({"role": "user", "content": user_message})

            # Check for inventory-related queries
            if "laptops" in user_message.lower():
                laptops = filter_by_category("laptop", inventory)
                if laptops:
                    laptop_names = ", ".join([laptop["name"] for laptop in laptops])
                    ai_message = f"We currently have the following laptops in stock: {laptop_names}."
                else:
                    ai_message = "Sorry, we currently have no laptops in stock."
                context.append({"role": "assistant", "content": ai_message})
                await manager.broadcast(f"AI: {ai_message}")
            elif "HP" in user_message or "Dell" in user_message:  # Specific brand query
                item = find_item_by_name(user_message, inventory)
                if item:
                    if item["quantity"] > 0:
                        ai_message = f"We have {item['quantity']} units of {item['name']} in stock."
                    else:
                        ai_message = f"Sorry, {item['name']} is currently out of stock."
                else:
                    ai_message = "I couldn't find that item in our inventory."
                context.append({"role": "assistant", "content": ai_message})
                await manager.broadcast(f"AI: {ai_message}")
            else:
                # Let OpenAI handle reasoning for complex queries
                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=context,
                        temperature=0.7,
                        max_tokens=150
                    )
                    ai_message = response.choices[0].message.content
                    context.append({"role": "assistant", "content": ai_message})
                    await manager.broadcast(f"AI: {ai_message}")
                except Exception as e:
                    error_message = f"Error generating response: {str(e)}"
                    print(error_message)
                    await websocket.send_text("AI: Sorry, there was an error generating a response.")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")
