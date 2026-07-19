from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agent import ACAgent
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=".ac Personal AI Assistant API")

# Setup CORS to allow any local frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the agent globally
agent = ACAgent()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    sources: list[str]

@app.get("/")
def read_root():
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
