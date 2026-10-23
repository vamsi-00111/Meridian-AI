from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config.settings import settings
from langchain_google_vertexai import VertexAIEmbeddings
from functools import lru_cache


@lru_cache(maxsize=1)
def embeddings():
    return  VertexAIEmbeddings(model_name=settings.embedding_model_name, project=settings.gcp_project_id, location=settings.gcp_region)