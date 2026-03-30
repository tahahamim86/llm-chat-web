from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from nhis_vector import retriever

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = OllamaLLM(model="llama3.2")

template = """
You are DoctorSina, an intelligent virtual doctor and a cutting-edge telemedicine platform. 
Use the following context to answer the user's question accurately. If the context doesn't have the answer, use your medical knowledge to answer helpfully, but prioritize the context when possible.

CRITICAL INSTRUCTIONS:
- DO NOT introduce yourself (e.g., "Hello, I am DoctorSina...") in every message.
- Only state your name or identity if the user explicitly asks "Who are you?" or "What is your name?".
- Answer their question directly and naturally, as you are in the middle of a continuous conversation.

Context:
{context}

Chat History:
{history_str}

Current Question:
{question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    question: str
    history: List[ChatMessage] = []

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    docs = retriever.invoke(req.question)
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # Format the history into a readable string for the prompt
    history_str = ""
    for msg in req.history:
        history_str += f"{msg.role.capitalize()}: {msg.content}\n"
        
    response = chain.invoke({
        "context": context, 
        "history_str": history_str,
        "question": req.question
    })
    return {"reply": response}
