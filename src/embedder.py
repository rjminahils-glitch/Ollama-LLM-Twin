import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CLEAN = Path("data/clean")

_model = None


def get_model() -> SentenceTransformer:
    """Load once, reuse. Loading takes seconds; embedding takes milliseconds."""
    global _model
    if _model is None:
        print(f"loading {MODEL_NAME} ...")
        _model = SentenceTransformer(MODEL_NAME)
        print(f"  dim={_model.get_sentence_embedding_dimension()}  "
              f"max_seq_length={_model.max_seq_length}")
    return _model


def embed(texts: list[str], batch_size: int = 32) -> np.ndarray:
    """Returns a normalised matrix, one row per text."""
    return get_model().encode(
        texts,
        batch_size=batch_size,
        convert_to_numpy=True,
        normalize_embeddings=True,      # so cosine == dot product
        show_progress_bar=len(texts) > 100,
    )


def search(query: str, matrix: np.ndarray, chunks: list[dict], k: int = 5) -> list[tuple[float, dict]]:
    q = embed([query])[0]
    scores = matrix @ q                 # one matmul, all similarities
    top = np.argsort(-scores)[:k]
    return [(float(scores[i]), chunks[i]) for i in top]


def load_chunks() -> list[dict]:
    path = CLEAN / "chunks.jsonl"
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]