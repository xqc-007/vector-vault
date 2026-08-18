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


class HealthResponse(BaseModel):
    status: str
