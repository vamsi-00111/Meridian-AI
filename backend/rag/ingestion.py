
import os
import shutil
import tempfile

from google.cloud import storage
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.settings import settings
from log import GLOBAL_LOGGER as log
from rag.vectorStore import vector_store

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100  


def split_into_chunks(pages: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    return splitter.split_documents(pages)


def ingest_pdf(local_path: str, source: str):
    pages = PyPDFLoader(local_path).load()

   
    for page in pages:
        page_number = str(page.metadata.get("page", 0))
        page.metadata = {
            "source": source,
            "page": page_number,
        }

    chunks = split_into_chunks(pages)

    if chunks:
        log.info(
            "Embedding chunks and pushing to Vector Search",
            source=source,
            chunks=len(chunks),
        )

        vector_store().add_documents(chunks)

        log.info(
            "Vector indexing completed",
            source=source,
            chunks=len(chunks),
        )

    return {"pages": len(pages), "chunks": len(chunks)}


def ingest_data_from_gcs() :
    log.info("Connecting to GCS bucket", bucket=settings.gcs_bucket_name)

    client = storage.Client(project=settings.gcp_project_id)
    blobs = client.bucket(settings.gcs_bucket_name).list_blobs(prefix=settings.gcs_prefix)

    totals = {"files": 0, "pages": 0, "chunks": 0}
    tmp_dir = tempfile.mkdtemp()
    try:
        for blob in blobs:
            if not blob.name.lower().endswith(".pdf"):
                continue
            local_path = os.path.join(tmp_dir, os.path.basename(blob.name))
            blob.download_to_filename(local_path)
            result = ingest_pdf(local_path, source=f"gs://{settings.gcs_bucket_name}/{blob.name}")
            log.info("Ingested PDF from GCS", blob=blob.name, **result)
            totals["files"] += 1
            totals["pages"] += result["pages"]
            totals["chunks"] += result["chunks"]
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    if totals["files"] == 0:
        log.warning("No PDF documents found in the specified bucket/prefix")
    log.info("Ingestion complete", **totals)
    return totals

        
    
    
