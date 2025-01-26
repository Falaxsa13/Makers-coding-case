from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.routes import inventory
from typing import List
from dotenv import load_dotenv
import os
from openai import OpenAI
import json
from utils.inventory import getProducts, createNewOrder, reply

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

# --------------------
# Define the OpenAI Functions (Schema + Description)
# --------------------
openai_functions = [
    {
        "name": "getProducts",
        "description": "Get details about products from inventory, including stock and price.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A query term. E.g., 'laptop' or 'dell'"
                }
            },
            "required": ["query"]
        },
    },
    {
        "name": "reply",
        "description": "Respond to the user's query with a final message.",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The response message to send to the user."
                }
            },
            "required": ["message"]
        }
    },
    {
        "name": "createNewOrder",
        "description": "Create a new order for a customer by deducting inventory.",
        "parameters": {
            "type": "object",
            "properties": {
                "customerId": {
                    "type": "integer",
                    "description": "The customer's ID"
                },
                "productId": {
                    "type": "integer",
                    "description": "The Product ID value of the product"
                },
                "quantity": {
                    "type": "integer",
                    "description": "How many units the customer wants"
                },
                "unitPrice": {
                    "type": "number",
                    "description": "Price per single unit"
                }
            },
            "required": ["customerId", "productId", "quantity", "unitPrice"]
        }
    }
]



# --------------------
# WebSocket Endpoint
# --------------------
@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful e-commerce assistant. "
                "You have access to a few specialized functions: getProducts, createNewOrder, and reply. "
                "Use them appropriately to help the user. "
                "Always check stock before confirming an order."
            )
        }
    ]

    try:
        while True:
            user_message = await websocket.receive_text()
            print(f"[User] {user_message}")

            # Add user message
            messages.append({"role": "user", "content": user_message})

            # Call OpenAI with function definitions
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                functions=openai_functions,
                function_call="auto"
            )

            
            msg_content = response.choices[0].message

            function_call = getattr(msg_content, "function_call", None)
            if function_call:
                # The AI wants to call a function
                function_name = msg_content.function_call.name
                arguments = msg_content.function_call.arguments

                try:
                    parsed_args = json.loads(arguments)
                except json.JSONDecodeError:
                    parsed_args = {}

                # Run the corresponding Python function
                function_response = None
                if function_name == "getProducts":
                    function_response = getProducts(**parsed_args)
                elif function_name == "createNewOrder":
                    function_response = createNewOrder(**parsed_args)
                elif function_name == "reply":
                    function_response = reply(**parsed_args)
                else:
                    function_response = "Function not recognized."

                # Now we give the function result back to the model as an assistant message with role=function
                messages.append({
                    "role": "function",
                    "name": function_name,
                    "content": function_response
                })

                # We call the model again to get the final user-facing text
                second_response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )
                final_content = second_response.choices[0].message.content

                messages.append({"role": "assistant", "content": final_content})
                await manager.broadcast(f"AI: {final_content}")

            else:
                # The AI did not call any function; it just responded with text
                final_content = msg_content.content
                messages.append({"role": "assistant", "content": final_content})
                await manager.broadcast(f"AI: {final_content}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")
