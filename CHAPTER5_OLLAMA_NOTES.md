# Chapter 5: From spreadsheet to dataset

## Concept: ETL pipeline
A data pipeline moves data from where humans put it (the Excel/Sheet) to where
machines can use it (JSONL), in three separated stages:
- **Extract** — read every row from the Excel tabs, don't judge it yet
- **Transform** — fix characters, drop drafts, standardise keys
- **Load** — write knowledge.jsonl and instructions.jsonl

Kept in separate functions so a change in one (e.g. someone renames a column)
never breaks the others.

## Rule: raw data is immutable
`data/raw/NUML_data_collection_template.xlsx` is raw and never edited by code.
`data/clean/knowledge.jsonl` and `data/clean/instructions.jsonl` are derived —
disposable, always rebuildable by re-running the script. One-way relationship:
`xlsx → build script → jsonl`, never the reverse.

## Deterministic + idempotent builds
Same input always produces the same output (no randomness, no relying on
dict ordering, no timestamps in the output). `save_jsonl` opens with `"w"`,
not `"a"`, so running the script 50 times gives one clean file, not 50
stacked copies.

## Schema: hybrid approach
- **Schema-on-write** (strict, reject at the door) — how the build script
  treats the data: required fields, category whitelist, length ranges.
- **Schema-on-read** (loose, accept anything, sort later) — how the Google
  Sheet works: fixed headers + dropdowns, but forgiving of half-finished rows.
- Golden rule: permissive at the human boundary (the sheet), strict at the
  machine boundary (the build script).

## The six data quality dimensions
Accuracy, Completeness, Consistency, Uniqueness, Validity, Timeliness.
Accuracy is the only one code can't check — that's why the reviewer role
exists and why nobody verifies their own rows.

## Files implemented this chapter
- `src/loaders.py` — `read_tab()` (EXTRACT), `to_knowledge()` / `to_instructions()`
  (TRANSFORM — keep only `status == verified` rows), `save_jsonl()` / `load_jsonl()`
  (LOAD), plus `clean()`, `normalise_header()`, `normalise_status()`, `make_title()`
  helpers.
- `src/validate.py` — `smoke_tests()` (whole-dataset checks), `validate_knowledge()`,
  `validate_instructions()` (per-row errors/warnings), `coverage()` (per-category
  knowledge-to-instruction ratio report).
- `src/build.py` — orchestrates EXTRACT → TRANSFORM → VALIDATE → LOAD, prints a
  full report, refuses to write output if smoke tests fail.

## Adapted from the chapter's example (not copied blindly)
The chapter's code used hardcoded macOS absolute paths
(`/Users/user/PycharmProjects/llm_twin/Data/cleann/`, with a typo — "cleann").
Adapted both to this project's existing relative structure from Chapter 2:
- `WORKBOOK = "data/raw/NUML_data_collection_template.xlsx"` (in `loaders.py`)
- `OUT_DIR = Path("data/clean/")` (in `build.py`)
- `CATEGORIES` in `validate.py` already matched this project's 8 categories
  (admissions, fees, programs, hostel, transport, scholarships, faculty,
  campus) — no change needed there.
- Added `openpyxl` to `requirements.txt`.

## Verified working
Built a small test workbook with a mix of `verified` and `draft` rows and ran
`python -m src.build` end to end: correctly read both tabs, correctly kept
only the verified row and skipped the draft row (reporting why), and correctly
refused to write output when the smoke test's minimum-entry threshold wasn't
met (exactly the intended fail-safe). Confirms the pipeline logic is sound
before running it against the real 135+135 entry NUML workbook.

## Steps to run this for real
1. `pip install -r requirements.txt` (adds openpyxl)
2. Download the Google Sheet: File → Download → Microsoft Excel (.xlsx)
3. Save it as `data/raw/NUML_data_collection_template.xlsx`
4. From the project root (not inside `src/`): `python -m src.build`
5. Read the EXTRACT/TRANSFORM/VALIDATE/LOAD report — fix any ERROR lines in
   the sheet (warnings are optional to fix), then re-run until clean
6. Check `data/clean/knowledge.jsonl` and `data/clean/instructions.jsonl` exist

## New vocabulary
ETL, raw vs. derived data, deterministic, idempotent, schema, referential
integrity, provenance.

## Status: Chapter 5 complete. Ran against the real NUML workbook — initially
97 validation errors (57 knowledge entries + 40 instruction answers under the
40-word minimum), fixed by expanding the sheet content, re-verified with a
clean 0 errors / 0 warnings run, confirmed deterministic across repeated runs.
Not yet pushed to GitHub — will push together with Chapter 4.

## Update: the sheet's own column headers specify 100-300 words for knowledge
text and 60-150 words for instruction output — a stricter bar than the
40-word floor above. `validate.py` was updated to enforce MIN_KNOWLEDGE_WORDS
= 100, MAX_KNOWLEDGE_WORDS = 300, MIN_ANSWER_WORDS = 60, MAX_ANSWER_WORDS =
150, and every knowledge entry and instruction answer was expanded again to
meet this tighter spec. Re-verified clean at 0 errors / 0 warnings against
the new thresholds.