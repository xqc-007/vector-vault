from fastapi import FastAPI, HTTPException

from backend.app.ingestion.chunker import chunk_text
from backend.app.ingestion.loader import load_document
from backend.app.retrieval.service import retrieval_service
from backend.app.schemas import (
    ChunkRequest,
    ChunkResponse,
    DocumentLoadRequest,
    DocumentLoadResponse,
    HealthResponse,
    IndexRequest,
    IndexResponse,
    SearchRequest,
    SearchResponse,
    SearchResult,
)


app = FastAPI(
    title="VectorVault",
    version="0.2.0",
    description="Document ingestion, embeddings and local vector search.",
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

    return ChunkResponse(chunk_count=len(chunks), chunks=chunks)


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


@app.post("/index", response_model=IndexResponse)
def index_text(request: IndexRequest):
    try:
        indexed = retrieval_service.index_text(
            text=request.text,
            source=request.source,
            chunk_size=request.chunk_size,
            overlap=request.overlap,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return IndexResponse(
        indexed_chunks=indexed,
        total_chunks=retrieval_service.store.count(),
    )


@app.post("/search", response_model=SearchResponse)
def search_vectors(request: SearchRequest):
    try:
        matches = retrieval_service.search(request.query, request.top_k)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    results = [
        SearchResult(
            text=match.text,
            source=match.source,
            chunk_index=match.chunk_index,
            score=match.score,
        )
        for match in matches
    ]

    return SearchResponse(
        result_count=len(results),
        results=results,
    )
