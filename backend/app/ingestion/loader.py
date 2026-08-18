from pathlib import Path


SUPPORTED_EXTENSIONS = {".txt", ".md"}


def load_document(path):
    """Load a supported text document from disk."""
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"document not found: {file_path}")

    if not file_path.is_file():
        raise ValueError("document path must point to a file")

    if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"unsupported file type: {file_path.suffix or 'unknown'}"
        )

    content = file_path.read_text(encoding="utf-8").strip()

    if not content:
        raise ValueError("document is empty")

    return content
