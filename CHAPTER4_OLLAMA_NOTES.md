# Chapter 4: Planning the LLM Twin's Data

## Two tracks needed for the twin
- Memory Track: raw factual knowledge, cut into passages of 200-500 words, needs BREADTH (many topics, accurate facts)
- Style Track: question/answer pairs written in a consistent voice, needs CONSISTENCY (one voice, 500+ pairs)

## Direction change during this chapter
Originally planned to build data/sources.json pointing at my own GitHub repos as
source material. Teacher redirected the assignment: instead of personal repos,
I'm building a real dataset for a NUML university assistant, using a shared
Google Sheet as the actual data source.

## The shared data collection sheet
Google Sheet "NUML_data_collection_template" with tabs:
- READ ME FIRST (rules)
- knowledge (Memory Track — standalone factual statements, no questions)
- instructions (Style Track — student question + answer pairs in an agreed voice)
- assignments (class roster: who owns which category + ID range)

### knowledge tab columns
id | category | title | text (100-300 words, facts only) | source (how confirmed) | written_by | status

### instructions tab columns
id | category | instruction (question as a real student would type it) | output (60-150 words, agreed voice) | source_ids | written_by | status

### The 7 rules
1. Every entry must make sense completely alone (name the subject, don't assume context)
2. One topic per row
3. knowledge tab = statements only, never questions
4. Type directly in the sheet, don't paste from Word (hidden characters)
5. Never press Enter inside a cell
6. Avoid exact dates that expire — say "usually opens in early September," not a hard date
7. If not sure a fact is true, don't write it — confirm first

### Agreed voice for the instructions tab
Address the student as "you." Direct answer first, then detail. 60-150 words.
No emojis, slang, or jokes. If a rule/number might have changed, say so and name
the office to contact. Never invent a number.

### Status workflow
I mark my own rows as `draft`. Only the reviewer (instructor) can change a row to
`verified`. Only verified rows are used by the twin.

## My assignment
All categories, NUML Islamabad main campus: admissions (adm-001 to adm-030),
fees (fee-031 to fee-040), programs (prog-041 to prog-055), hostel
(host-056 to host-080), transport (trans-081 to trans-095), scholarships
(schol-096 to schol-110), faculty (fac-111 to fac-120), campus
(camp-121 to camp-135).

## Work completed this chapter
- All 30 admissions knowledge entries (adm-001 to adm-030) written and pasted
  into the sheet, sourced from official numl.edu.pk pages (admission portal,
  FAQs, eligibility PDFs, admission policy documents)
- All 10 fees knowledge entries (fee-031 to fee-040) written and pasted
- All 15 programs knowledge entries (prog-041 to prog-055) written and pasted
- All 25 hostel knowledge entries (host-056 to host-080) written and pasted
- All 15 transport knowledge entries (trans-081 to trans-095) written and pasted
- All 15 scholarships knowledge entries (schol-096 to schol-110) written and pasted
- All 10 faculty knowledge entries (fac-111 to fac-120) written and pasted
- All 15 campus knowledge entries (camp-121 to camp-135) written and pasted
- All 135 matching instructions (Q&A pairs) written, following the agreed voice
- No fact invented without a source; fee amounts and other figures that change
  every semester were written as "check the official portal" rather than a hard
  number, per rule 6/7

## Data volume decision (RAG vs fine-tuning)
135 knowledge entries + 135 instruction pairs = solidly in the chapter's
"50–200 documents" sweet spot. Decision: combine RAG (facts, Memory Track)
with fine-tuning (voice, Style Track), per the chapter's guidance table.

## Source-collection table (N/A this chapter)
The chapter's source-collection table (blog, Medium, GitHub API, LinkedIn
export, etc.) doesn't apply here — my data source isn't personal writing
scraped from platforms, it's the shared NUML Google Sheet, exported to CSV.

## sources.json updated
data/sources.json no longer points at personal GitHub repos (the chapter's
example uses "type": "article"/"repository" for a student's own blog/GitHub).
Since my source is the NUML Google Sheet exported to CSV rather than GitHub,
mine uses "type": "sheet" pointing at data/raw/knowledge.csv and
data/raw/instructions.csv, each tagged with all 8 categories and
written_by_me set to true — no external contributors.

## Status: Chapter 4 complete, sources.json pushed to GitHub