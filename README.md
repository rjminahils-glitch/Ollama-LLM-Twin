## Progress So Far

- **Chapter 1** — Course overview: two core jobs for the twin — Memory (facts/knowledge) and Style (voice/tone)
- **Chapter 2** — Environment setup: Ollama installed, llama3.2:3b model downloaded, Python venv + dependencies, project structure created and verified
- **Chapter 3** — Sampling controls (temperature/top_p/num_predict), streaming responses (`ask_stream()`), conversation memory (`Chat` class with `send()`/`reset()`)
- **Chapter 4** — Data collection: defined Memory Track (factual knowledge) vs Style Track (Q&A voice pairs), researched and wrote entries across admissions, fees, programs, hostel, transport, scholarships, faculty, and campus from official NUML sources, built `data/sources.json` cataloging the dataset
- **Chapter 5** — ETL pipeline: built `src/loaders.py`, `src/validate.py`, `src/build.py` to extract the NUML workbook, validate every entry (length, category, referential integrity), and load clean `data/clean/knowledge.jsonl` / `instructions.jsonl`. All 135 knowledge entries and 135 instruction pairs pass validation with 0 errors.
- **Chapter 6** — Chunking: built `src/chunk.py` and `src/build_chunks.py` to split knowledge entries into retrieval-sized chunks with sentence-boundary overlap, enrich each chunk's embed text with category context, and carry `chunk_id`/`source_id` for traceability back to the original spreadsheet row. 135 entries produced 135 chunks (none needed splitting).
- **Post-Chapter 6 fix** — found that `validate.py`'s 40-word minimum was looser than the sheet's own column-header spec (100-300 words for knowledge text, 60-150 for instruction output); tightened the validator to match, then expanded all 135 knowledge entries and 135 instruction answers to genuinely meet it. Re-verified clean at 0 errors, 0 warnings, 135 chunks.

See the `CHAPTER*_OLLAMA_NOTES.md` files for detailed notes on each chapter.

All code and dataset content in this project was researched, written, and verified by me. No external contributors.

## Setup

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Requires [Ollama](https://ollama.com) installed locally with the `llama3.2:3b` model pulled:

```powershell
ollama pull llama3.2:3b
```

## Status

Work in progress — following a chapter-by-chapter course structure. Chapters 1–6 complete, awaiting Chapter 7.