from langchain_google_vertexai import VectorSearchVectorStore
from google.cloud import aiplatform
from config.settings import settings
from rag.embeddings import embeddings



def vector_store():
    
    aiplatform.init(project=settings.gcp_project_id,location=settings.gcp_region)
    
    return VectorSearchVectorStore.from_components(
        project_id=settings.gcp_project_id,
        region=settings.gcp_region,
        gcs_bucket_name=settings.gcs_bucket_name,
        index_id=settings.vector_search_index_id,
        endpoint_id=settings.vector_search_index_endpoint_id,
        embedding=embeddings()   
        
    )
        
    