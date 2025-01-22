from langchain_groq import ChatGroq
import os

def setup_chat_model():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set")
        
    return ChatGroq(
        api_key=api_key,
        model='llama3-70b-8192',
        temperature=0
    )