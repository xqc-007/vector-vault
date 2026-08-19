from pydantic import BaseModel, Field


class ChunkRequest(BaseModel):
    text: str = Field(min_length=1)
    chunk_size: int = Field(default=500, gt=0)
    overlap: int = Field(default=50, ge=0)


class ChunkResponse(BaseModel):
    chunk_count: int
    chunks: list[str]


class DocumentLoadRequest(BaseModel):
    path: str = Field(min_length=1)


class DocumentLoadResponse(BaseModel):
    path: str
    character_count: int
    content: str


class IndexRequest(BaseModel):
    text: str = Field(min_length=1)
    source: str = Field(default="manual", min_length=1)
    chunk_size: int = Field(default=500, gt=0)
    overlap: int = Field(default=50, ge=0)


class IndexResponse(BaseModel):
    indexed_chunks: int
    total_chunks: int


class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=5, gt=0, le=20)


class SearchResult(BaseModel):
    text: str
    source: str
    chunk_index: int
    score: float


class SearchResponse(BaseModel):
    result_count: int
    results: list[SearchResult]


class HealthResponse(BaseModel):
    status: str
