## Progress So Far

- **Chapter 1** — Course overview: two core jobs for the twin — Memory (facts/knowledge) and Style (voice/tone)
- **Chapter 2** — Environment setup: Ollama installed, llama3.2:3b model downloaded, Python venv + dependencies, project structure created and verified
- **Chapter 3** — Sampling controls (temperature/top_p/num_predict), streaming responses (`ask_stream()`), conversation memory (`Chat` class with `send()`/`reset()`)
- **Chapter 4** — Data collection: defined Memory Track (factual knowledge) vs Style Track (Q&A voice pairs), researched and wrote entries across admissions, fees, programs, hostel, transport, scholarships, faculty, and campus from official NUML sources, built `data/sources.json` cataloging the dataset
- **Chapter 5** — ETL pipeline: built `src/loaders.py`, `src/validate.py`, `src/build.py` to extract the NUML workbook, validate every entry (length, category, referential integrity), and load clean `data/clean/knowledge.jsonl` / `instructions.jsonl`. All 135 knowledge entries and 135 instruction pairs pass validation with 0 errors.

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

Work in progress — following a chapter-by-chapter course structure. Chapters 1–5 complete, awaiting Chapter 6.