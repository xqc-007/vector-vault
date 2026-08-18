# Retrieval Notes

A retrieval system tries to find the most relevant pieces of information for a user query.

A basic retrieval pipeline usually starts by loading documents and splitting them into smaller chunks. Those chunks can later be converted into vector embeddings.

The quality of retrieval depends on more than the embedding model. Chunk size, overlap, ranking logic, and evaluation all affect the final result.

VectorVault starts with ingestion and chunking so each later stage can be tested independently.
