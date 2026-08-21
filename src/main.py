from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.agent import ACAgent
import os

app = FastAPI(title=".ac Personal AI Assistant API")

# Setup CORS to allow any local frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the frontend directory statically
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")


# Initialize the agent globally
agent = ACAgent()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    sources: list[str]

@app.get("/")
def read_root():
    # Serve the main index.html for the web app UI
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"status": "error", "message": "Frontend not found"}

@app.get("/health")
def read_health():
    return {
        "status": "online",
        "message": "Welcome to the .ac Personal AI Brain. System is ready."
    }

@app.post("/chat", response_model=ChatResponse)
def chat_with_agent(request: ChatRequest):
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty.")

        result = agent.ask(request.message)

        return ChatResponse(
            reply=result.get("answer", ""),
            sources=result.get("sources", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Note: Run this with `uvicorn src.main:app --reload --host 0.0.0.0 --port 8000`
