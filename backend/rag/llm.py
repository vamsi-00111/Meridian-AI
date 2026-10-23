from config.settings import settings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq





def chat_model():

    #return  ChatGoogleGenerativeAI(model=settings.llm_model_name, google_api_key=settings.google_api_key)
    llm = ChatGroq(
    model=settings.llm_model_name,
    api_key=settings.groq_api_key,
    temperature=0,
    max_tokens=700,
    max_retries=3,
)
    return llm
    



def extract_text(content) -> str:
   
    if isinstance(content, list):
        return "\n".join(
            block.get("text", "") for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )
    return content

