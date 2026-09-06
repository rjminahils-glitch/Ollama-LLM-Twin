import numpy as np
from src.embedder import embed, load_chunks, CLEAN

chunks = load_chunks()
print(f"embedding {len(chunks)} chunks")

matrix = embed([c["embed_text"] for c in chunks])
np.save(CLEAN / "embeddings.npy", matrix)

print(f"saved {matrix.shape} -> embeddings.npy")
print(f"  vector norms: {np.linalg.norm(matrix, axis=1).mean():.4f} (should be 1.0)")
print(f"  file size: {matrix.nbytes / 1024:.0f} KB")