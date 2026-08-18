from fastapi import FastAPI, HTTPException

from backend.app.ingestion.chunker import chunk_text
from backend.app.ingestion.loader import load_document
from backend.app.schemas import (
    ChunkRequest,
    ChunkResponse,
    DocumentLoadRequest,
    DocumentLoadResponse,
    HealthResponse,
)


app = FastAPI(
    title="VectorVault",
    version="0.1.0",
    description="Document ingestion and chunking foundation for VectorVault.",
)


@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="ok")


@app.post("/chunks", response_model=ChunkResponse)
def create_chunks(request: ChunkRequest):
    try:
        chunks = chunk_text(
            request.text,
            chunk_size=request.chunk_size,
            overlap=request.overlap,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return ChunkResponse(
        chunk_count=len(chunks),
        chunks=chunks,
    )


@app.post("/documents/load", response_model=DocumentLoadResponse)
def load_local_document(request: DocumentLoadRequest):
    try:
        content = load_document(request.path)
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return DocumentLoadResponse(
        path=request.path,
        character_count=len(content),
        content=content,
    )
