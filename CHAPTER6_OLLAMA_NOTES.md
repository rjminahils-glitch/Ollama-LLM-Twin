# Chapter 6: Chunking

## Three reasons to chunk (not just one)
1. **Context window** (the obvious one) — a model can't process an entire
   document at once; there's a hard limit on how much text it can "see."
2. **Retrieval precision** (the one that matters most here) — if the whole
   knowledge base is one giant document, retrieval pulls back that whole
   document for any matching query, burying the one relevant sentence in
   thousands of irrelevant words.
3. **Embedding dilution** (the deepest reason) — an embedding is one vector
   summarizing a passage's meaning. A passage covering ten topics produces a
   vector that's an "average" of all ten — not close to any of them. Small,
   focused chunks get sharp, precise vectors instead of "mush." This is why
   "just use a bigger context window" doesn't solve the underlying problem.

## The precision-context tradeoff
- Chunks **too small**: facts get separated from their exceptions/context
  (e.g. a rule in one chunk, its exception in another); retrieval returns
  fragments instead of complete ideas.
- Chunks **too large**: retrieved text is mostly irrelevant noise, the
  embedding gets diluted across topics, and context window space is wasted
  on filler instead of useful information.
- No universally correct chunk size — "512 tokens, 50 overlap" is a starting
  guess, not a rule. The right size depends on how the data is organized.

## The four chunking strategies (crude to smart)
1. **Fixed-size** — cut every N characters, ignoring structure. Crude, fast,
   slices sentences in half.
2. **Sliding window with overlap** — like fixed-size, but repeats the last
   ~50 words of the previous chunk so boundary facts aren't lost. Costs more
   storage, creates near-duplicate retrievals.
3. **Recursive character splitting** — tries paragraph breaks first, then
   sentence ends, then spaces. LangChain's default splitter; sensible
   general-purpose choice.
4. **Semantic chunking** — embed each sentence, cut where consecutive
   sentences become topically dissimilar. Most principled, but expensive —
   "the juice isn't worth the squeeze" for this project's scale.

## Traceability
Every chunk carries the `source_id` of the entry it came from, so a wrong
answer can be traced: wrong answer -> retrieved chunk -> source entry ->
spreadsheet row -> the student who wrote it. Without this, a bug is just
"the AI is broken." With it, it's "row 47 has a typo" — fixable directly.

## Files implemented this chapter
- `src/chunk.py` — `split_long_text()` (sentence-boundary splitting with
  overlap, only triggers above `MAX_WORDS = 220`), `is_auto_title()` (skips
  repeating a title in the embedded text if the title was just auto-generated
  from the text itself), `enrich()` (builds the embed-text: category context
  first, then title if it adds anything, then the fact), `build_chunks()`
  (produces the final chunk records with `chunk_id`/`source_id` for
  traceability), `chunk_report()` (prints word-count stats and flags).
- `src/build_chunks.py` — reads `data/clean/knowledge.jsonl`, builds chunks,
  writes `data/clean/chunks.jsonl`, prints a report plus 3 example chunks.

## Adapted from the chapter's example (not copied blindly)
- `CLEAN` path in `build_chunks.py`: chapter used a hardcoded macOS absolute
  path (`Data/cleann/`, with a typo) -> changed to `Path("data/clean")`,
  matching this project's existing folder from Chapter 5.
- `CATEGORY_CONTEXT` in `chunk.py` already matched this project's 8
  categories (admissions, fees, programs, hostel, transport, scholarships,
  faculty, campus) exactly — no change needed.
- No new dependencies — `chunk.py`/`build_chunks.py` only use the standard
  library (`json`, `re`, `collections`, `pathlib`), so `requirements.txt`
  is unchanged this chapter.

## Verified working
Ran `python -m src.build_chunks` against the real, already-fixed
`knowledge.jsonl` (135 entries, all 40-99 words after Chapter 5's length
fixes): produced exactly 135 chunks — none needed splitting, since every
entry is well under the 220-word `MAX_WORDS` threshold. No "short entry"
notes either, since Chapter 5's 40-word minimum is already above this
chapter's 15-word `SHORT_WORDS` flag. Spot-checked 3 example chunks and
confirmed `embed_text` correctly prepends the category context sentence
(e.g. "NUML admissions, eligibility and entry test.") before the fact.

## Steps to run this for real
1. No new pip installs needed this chapter
2. Make sure `data/clean/knowledge.jsonl` exists (from Chapter 5's
   `python -m src.build`)
3. From the project root: `python -m src.build_chunks`
4. Check the printed report: chunk count, word-count min/median/max for
   both `text` and `embed_text`, category breakdown, and any notes about
   entries that got split or flagged as short
5. Confirm `data/clean/chunks.jsonl` was created

## New vocabulary
Context window, retrieval precision, embedding dilution, chunk, overlap,
recursive character splitting, semantic chunking, traceability, enrichment.

## Status: Chapter 6 implemented and verified against the real, already-fixed
knowledge.jsonl (135 entries -> 135 chunks, 0 splits needed). Not yet pushed
to GitHub.