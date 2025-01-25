from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import inventory

app = FastAPI()

# Allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(inventory.router, prefix="/api/inventory", tags=["Inventory"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the ChatBot Backend!"}
