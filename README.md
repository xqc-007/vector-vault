# VectorVault

VectorVault is a document retrieval project focused on building the foundations of a retrieval-augmented generation system from the ground up.

## Status

**Active development**

The current version focuses only on document ingestion and chunking.

No embeddings, vector database, or LLM generation has been added yet.

## Current features

- load plain-text and Markdown documents
- validate supported file types
- split documents into overlapping text chunks
- expose ingestion and chunking through FastAPI
- Pydantic request/response validation
- automated tests with pytest

## Planned next steps

- embedding provider
- cosine similarity search
- local vector storage
- retrieval API
- retrieval evaluation
- cited answer generation
- optional LLM integration

## Project structure

```text
vector-vault/
├── backend/
│   ├── app/
│   │   ├── ingestion/
│   │   │   ├── __init__.py
│   │   │   ├── chunker.py
│   │   │   └── loader.py
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── schemas.py
│   └── tests/
│       ├── __init__.py
│       ├── test_api.py
│       ├── test_chunker.py
│       └── test_loader.py
├── data/
│   └── sample_docs/
│       └── retrieval_notes.md
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run the API

From the project root:

```bash
uvicorn backend.app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## Run the tests

```bash
pytest
```

## Current API

### Health check

```text
GET /health
```

### Chunk text

```text
POST /chunks
```

Example body:

```json
{
  "text": "Vector search compares a query embedding with document embeddings.",
  "chunk_size": 60,
  "overlap": 10
}
```

### Load a local sample document

```text
POST /documents/load
```

Example body:

```json
{
  "path": "data/sample_docs/retrieval_notes.md"
}
```

## Why this project

The goal is to understand and implement the pieces behind retrieval systems instead of starting with a framework that hides the retrieval pipeline.

The first milestone is intentionally small: get document ingestion and chunking correct before adding embeddings and search.
