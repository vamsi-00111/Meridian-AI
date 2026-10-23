from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import Field
import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

class SecretKeys(BaseSettings):
    
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT/".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )
    
    
    project_name: str = Field("", alias="PROJECT_NAME")

    gcp_region: str = Field("", alias="GCP_REGION")
    gcp_project_id: str = Field("", alias="GCP_PROJECT_ID")
    gcs_bucket_name: str = Field("", alias="GCS_BUCKET_NAME")
    gcs_prefix: str = Field("", alias="GCS_PREFIX")
    google_api_key: str = Field("", alias="GOOGLE_API_KEY")
    gcp_service_account_path: str = Field("", alias="GCP_SERVICE_ACCOUNT_PATH")
    
    
    groq_api_key: str = Field("", alias="GROQ_API_KEY")

    llm_model_name: str = Field(
        validation_alias="MODEL_NAME"
    )
    embedding_model_name: str = Field(
        "text-embedding-005",
        validation_alias="VERTEX_EMBEDDING_MODEL_NAME"
    )

    vector_search_index_id: str = Field(
        "",
        validation_alias="VECTOR_SEARCH_INDEX_ID"
    )
    vector_search_index_endpoint_id: str = Field(
        "",
        validation_alias="VECTOR_SEARCH_INDEX_ENDPOINT_ID"
    )

    
    

settings=SecretKeys()

if settings.gcp_service_account_path:
    abs_path = os.path.abspath(settings.gcp_service_account_path)
    if os.path.exists(abs_path):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = abs_path

