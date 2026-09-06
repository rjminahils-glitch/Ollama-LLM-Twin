import numpy as np
from src.embedder import search, load_chunks, CLEAN

chunks = load_chunks()
matrix = np.load(CLEAN / "embeddings.npy")

QUERIES = [
    "how much do i have to pay",
    "where is numl",
    "can i get a room in hostel",
    "is there a bus service",
    "what marks do i need for bscs",
    "money help for poor students",
]

for q in QUERIES:
    print(f"\nQ: {q}")
    for score, c in search(q, matrix, chunks, k=3):
        print(f"  [{score:.3f}] {c['chunk_id']} ({c['category']})  {c['text'][:75]}")