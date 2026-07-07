from langchain_openai import ChatOpenAI
from app.config import API_KEY,BASE_URL
def load_llm(model_name):
    model=ChatOpenAI(model=model_name,
                     base_url=BASE_URL,
                     api_key=API_KEY,
                     temperature=0.7)
    return model
