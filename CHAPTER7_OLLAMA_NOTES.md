# Chapter 7: Embeddings

## The vocabulary mismatch problem
A student types "how much do I have to pay" but the knowledge base says
"Semester fees are due within the first two weeks." Not one content word is
shared, yet the two mean the same thing. Keyword search would miss this
entirely. Embeddings close this gap by mapping meaning, not words, into a
shared numeric space.

## What an embedding is
A function `f(text) -> R^d` that maps any piece of text (short or long) to a
fixed-length vector. For our model, d = 384 — every chunk becomes exactly
384 numbers, no matter its word count. The defining property: texts with
similar meaning map to nearby vectors, even sharing zero words. Unlike
word2vec (one vector per word, no context), modern embeddings are
transformer-based and read the whole sentence, so "bank" (river) and "bank"
(money) get different vectors depending on context.

## How the model learned this: contrastive training
Trained on positive pairs (question+answer, title+article, paraphrases) and
negative pairs (other texts in the same batch), using a loss function
(InfoNCE / multiple-negatives-ranking) that pushes related texts' cosine
similarity up and unrelated texts' similarity down. Two consequences worth
remembering:
1. **Geometry is inherited from training pairs** — a model trained on Q&A
   pairs is the right choice for a Q&A-shaped task like ours (casual student
   questions -> formal knowledge base entries).
2. **The model never memorizes your data** — it's frozen; our 135 chunks are
   just points placed in its existing 384-dimensional space, using rules
   learned from billions of other texts. We don't retrain it.

## Why cosine similarity (not Euclidean or dot product)
Euclidean distance and dot product are both sensitive to vector length,
and vector length tends to correlate with text length/word frequency — so a
99-word admissions chunk could look "more similar" than a 10-word library
chunk just by being longer, regardless of actual meaning. Cosine similarity
only measures the angle between vectors, ignoring magnitude, so a short
fact and a long fact compete fairly on meaning alone.

**Normalization trick**: if every vector is scaled to unit length (norm =
1), cosine similarity becomes a plain dot product (`cos(a,b) = a·b` when
`||a||=||b||=1`) — much cheaper to compute at scale. This is why
`embed()` passes `normalize_embeddings=True`.

## Score interpretation (from the chapter's table)
| Cosine score | Meaning |
|---|---|
| > 0.7 | Near-paraphrase |
| 0.5 - 0.7 | Strongly related (target zone) |
| 0.3 - 0.5 | Loosely related, weak connection |
| < 0.3 | Probably unrelated |

## Sequence length limit
`all-MiniLM-L6-v2` truncates silently at 256 word-pieces (~180-200 English
words) — no error, just quietly drops anything past the limit. Our longest
enriched chunk is well under 200 words, so nothing is truncated.

## Bi-encoder vs cross-encoder
Bi-encoders embed queries and documents independently, so documents can be
pre-computed once and search is a single fast matrix multiply — this is
what we're building. Cross-encoders score a query+document pair together
(more accurate, but can't be pre-computed, doesn't scale to 135+ chunks at
query time). We use a bi-encoder for retrieval, matching the chapter's
recommendation.

## Files implemented this chapter
- `src/embedder.py` — `get_model()` (loads `all-MiniLM-L6-v2` once, cached
  globally), `embed()` (returns a normalized matrix so cosine == dot
  product), `search()` (embeds the query, does one matmul against the
  stored matrix, returns top-k by score), `load_chunks()` (reads
  `data/clean/chunks.jsonl`).
- `src/build_embeddings.py` — embeds every chunk's `embed_text`, saves the
  matrix to `data/clean/embeddings.npy`, prints shape/norm/file-size stats.
- `src/try_search.py` — loads the saved embeddings and runs 6 sample
  queries through `search()`, printing the top-3 matches for each.

## Adapted from the chapter's example (not copied blindly)
- `CLEAN` path in `embedder.py`: chapter used a hardcoded macOS absolute
  path (`Data/cleann/`, with a typo) -> changed to `Path("data/clean")`,
  matching this project's existing convention from Chapters 5-6.
- Model choice (`all-MiniLM-L6-v2`), normalization, and the search math
  were used exactly as given — no changes needed.
- `sentence-transformers` was already in `requirements.txt` from Chapter 2,
  so no dependency changes this chapter.

## Verified working
Ran `python -m src.build_embeddings` against the real 135 chunks:
`dim=384`, `max_seq_length=256` (both match the chapter exactly), vector
norms = 1.0000 (confirms normalization), output `(135, 384)` at 202 KB.

Ran `python -m src.try_search` with the chapter's 6 sample queries. Every
query retrieved the correct category on top despite little or no word
overlap with the matching chunk (e.g. "money help for poor students" ->
scholarships, "is there a bus service" -> transport). Honest note: by the
chapter's own score table, only 2 of 6 top matches landed in the 0.5-0.7
"target zone" (where is numl: 0.670, what marks for bscs: 0.542); the other
4 landed in the 0.3-0.5 "loosely related" band, including "how much do i
have to pay" at 0.347. Retrieval picked the right category every time, but
the absolute scores ran lower than the chapter's example suggested — likely
a property of this specific dataset's formal phrasing vs. very casual test
queries, not a bug in the code. Worth keeping in mind for later chapters
that may touch re-ranking or chunk enrichment.

## Steps to run this for real
1. No new pip installs needed this chapter (`sentence-transformers` was
   already in `requirements.txt`)
2. Make sure `data/clean/chunks.jsonl` exists (from Chapter 6's
   `python -m src.build_chunks`)
3. From the project root: `python -m src.build_embeddings` (first run
   downloads the ~90MB model from HuggingFace, needs internet)
4. Confirm `data/clean/embeddings.npy` was created, and check the printed
   dim/max_seq_length/norm/size stats
5. Run `python -m src.try_search` and read the top-3 results per query

## New vocabulary
Embedding, vector, vocabulary mismatch, contrastive learning, positive/
negative pairs, InfoNCE loss, cosine similarity, normalization, sequence
length limit, word-piece, bi-encoder, cross-encoder.

## Status: Chapter 7 implemented and verified against the real 135 chunks.
Pushed to GitHub (commit 57a8be3).