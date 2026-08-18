import pytest

from backend.app.ingestion.chunker import chunk_text


def test_chunk_text_returns_single_chunk_for_short_text():
    chunks = chunk_text(
        "Vector search finds semantically similar text.",
        chunk_size=100,
        overlap=10,
    )

    assert chunks == [
        "Vector search finds semantically similar text."
    ]


def test_chunk_text_creates_overlapping_chunks():
    text = "abcdefghijklmnopqrstuvwxyz"

    chunks = chunk_text(
        text,
        chunk_size=10,
        overlap=2,
    )

    assert chunks[0] == "abcdefghij"
    assert chunks[1].startswith("ij")
    assert len(chunks) > 1


def test_chunk_text_rejects_empty_text():
    with pytest.raises(ValueError):
        chunk_text("")


def test_chunk_text_rejects_invalid_overlap():
    with pytest.raises(ValueError):
        chunk_text(
            "some text",
            chunk_size=20,
            overlap=20,
        )
