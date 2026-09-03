import json
from pathlib import Path
from src.chunk import build_chunks, chunk_report

# Adapted from the chapter's absolute macOS path ("Data/cleann/", note the
# typo) to this project's existing data/clean/ folder, same as build.py in
# Chapter 5.
CLEAN = Path("data/clean")

entries = [json.loads(l) for l in (CLEAN / "knowledge.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
chunks, notes = build_chunks(entries)

with open(CLEAN / "chunks.jsonl", "w", encoding="utf-8") as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")

print(f"{len(entries)} entries -> {len(chunks)} chunks\n")
chunk_report(chunks, notes)

print("\n--- 3 examples of what gets embedded ---")
for c in sorted(chunks, key=lambda c: len(c["text"].split()))[:3]:
    print(f"\n{c['chunk_id']}")
    print(f"  shown   : {c['text']}")
    print(f"  embedded: {c['embed_text']}")