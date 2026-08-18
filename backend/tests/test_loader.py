from pathlib import Path

import pytest

from backend.app.ingestion.loader import load_document


def test_load_document_reads_text_file(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("hello vector vault", encoding="utf-8")

    content = load_document(file_path)

    assert content == "hello vector vault"


def test_load_document_rejects_missing_file(tmp_path):
    missing_path = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError):
        load_document(missing_path)


def test_load_document_rejects_unsupported_file_type(tmp_path):
    file_path = tmp_path / "sample.csv"
    file_path.write_text("a,b,c", encoding="utf-8")

    with pytest.raises(ValueError):
        load_document(file_path)
