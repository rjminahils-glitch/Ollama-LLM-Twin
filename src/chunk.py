import json
import re
from collections import Counter
from pathlib import Path

MAX_WORDS = 220          # above this, split
OVERLAP_WORDS = 40       # repeated context when we do split
SHORT_WORDS = 15         # below this, note it as low signal

CATEGORY_CONTEXT = {
    "admissions":   "NUML admissions, eligibility and entry test",
    "fees":         "NUML fees, payment and financial matters",
    "programs":     "NUML degree programs and departments",
    "hostel":       "NUML hostel accommodation and residence rules",
    "transport":    "NUML transport and shuttle service",
    "scholarships": "NUML scholarships and financial aid",
    "faculty":      "NUML faculty, staff and university history",
    "campus":       "NUML campus, facilities and student services",
}


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


def split_long_text(text: str, max_words: int = MAX_WORDS, overlap: int = OVERLAP_WORDS) -> list[str]:
    """Split on sentence boundaries with overlap. Most entries pass through untouched."""
    if len(text.split()) <= max_words:
        return [text]

    pieces, current, count = [], [], 0
    for sentence in split_sentences(text):
        n = len(sentence.split())
        if count + n > max_words and current:
            pieces.append(" ".join(current))
            tail = " ".join(current).split()[-overlap:]
            current, count = [" ".join(tail)], len(tail)
        current.append(sentence)
        count += n
    if current:
        pieces.append(" ".join(current))
    return pieces


def is_auto_title(title: str, text: str) -> bool:
    """True if the title was generated from the text and would only repeat it."""
    if not title:
        return True
    t = title.rstrip(".").strip().lower()
    return text.strip().lower().startswith(t[:25])


def enrich(title: str, category: str, text: str) -> str:
    """The text we embed: context first, then the fact."""
    parts = [CATEGORY_CONTEXT.get(category, category) + "."]
    if not is_auto_title(title, text):
        parts.append(title.strip().rstrip(".") + ".")
    parts.append(text)
    return " ".join(parts)


def build_chunks(entries: list[dict]) -> tuple[list[dict], list[str]]:
    chunks, notes = [], []

    for e in entries:
        pieces = split_long_text(e["text"])
        if len(pieces) > 1:
            notes.append(f"{e['id']}: split into {len(pieces)} chunks ({len(e['text'].split())} words)")

        for i, piece in enumerate(pieces):
            words = len(piece.split())
            if words < SHORT_WORDS:
                notes.append(f"{e['id']}: only {words} words, relying on enrichment")

            chunks.append({
                "chunk_id": f"{e['id']}#{i}" if len(pieces) > 1 else e["id"],
                "source_id": e["id"],
                "category": e["category"],
                "title": e.get("title", ""),
                "text": piece,                                                   # shown to the user
                "embed_text": enrich(e.get("title", ""), e["category"], piece),   # embedded
                "written_by": e.get("written_by", "unknown"),
            })
    return chunks, notes


def chunk_report(chunks: list[dict], notes: list[str]) -> None:
    T = sorted(len(c["text"].split()) for c in chunks)
    E = sorted(len(c["embed_text"].split()) for c in chunks)
    mid = len(T) // 2
    print(f"chunks: {len(chunks)}")
    print(f"  shown text  min={T[0]:>3} median={T[mid]:>3} max={T[-1]:>3}")
    print(f"  embed text  min={E[0]:>3} median={E[mid]:>3} max={E[-1]:>3}")
    print("  by category:", dict(sorted(Counter(c["category"] for c in chunks).items())))

    unknown = {c["category"] for c in chunks} - set(CATEGORY_CONTEXT)
    if unknown:
        print(f"  WARNING: no enrichment phrase for {sorted(unknown)}")

    if notes:
        print(f"\n  notes ({len(notes)}):")
        for n in notes[:10]:
            print("   -", n)