import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.chatbot import Chatbot

app = FastAPI()
bot = Chatbot()

# ✅ Allow frontend (Streamlit) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in prod, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Health check endpoint (ADD THIS)
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "StudyBuddy API"}

# ✅ Define input model for POST body
class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
async def chat(request: ChatRequest):
    reply = bot.generate_response(request.prompt)
    return {"response": reply}