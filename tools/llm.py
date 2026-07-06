from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key=os.environ.get("GROQ_API_KEY")

def load_llm():
    model=ChatOpenAI(model="llama-3.3-70b-versatile",
                     base_url="https://api.groq.com/openai/v1",
                     api_key=api_key,
                     temperature=0.5)
    return model
