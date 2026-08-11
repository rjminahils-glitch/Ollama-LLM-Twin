# Chapter 3: Controlling the Model from Python

## What was missing after Chapter 2
The `ask()` function could only send a prompt and get a full paragraph back.
Three gaps: no control over randomness, no conversation memory, no structured output (that's Chapter 11).

## 1. Sampling parameters

| Parameter    | What it controls                                  | Value used |
|--------------|-----------------------------------------------------|------------|
| temperature  | How random/creative vs predictable the output is    | 0.7        |
| top_p        | Only consider words whose probabilities sum to top_p| 0.9        |
| num_predict  | Max tokens generated (~0.75 words/token)             | 500        |

- 0.0 temperature → always picks the most likely word (robotic)
- 1.0 temperature → picks randomly (chaotic)
- 0.7 → balanced, creative but sensible

Passed via `options={...}` in `ollama.chat()`.

## 2. Streaming

Without streaming: wait in silence, then the full answer appears at once.
With streaming (`stream=True`): iterate over `ollama.chat(...)`, printing each
chunk's `chunk["message"]["content"]` as it arrives — feels like someone typing.

Implemented in `ask_stream()` in `src/llm.py`. Verified: `python -m src.test_stream`
prints gradually, no errors.

## 3. Conversation memory

The model has no memory between calls — it's stateless. "Remembering" is just:
append every turn (user + assistant) to a `messages` list and resend the *whole*
list every time.

Consequences:
- Cost and latency grow with conversation length (every turn reprocesses full history)
- Eventually breaks: exceed the context window and the earliest messages must be
  dropped or summarized

Implemented as a `Chat` class in `src/chat.py`:
- `__init__`: stores `system` message (if any) as the first entry in `self.messages`
- `send()`: appends the user prompt, calls `ollama.chat()` with the full history,
  appends the assistant's reply, returns it
- `reset()`: keeps the system message (if present), wipes the rest

Verified: `python -m src.test_chat` — second question ("How is it different from
Postgres?") correctly resolved "it" as vector database, proving history was resent.

## Files added/changed this chapter
- `src/llm.py` — added `options` params to `ask()`, added `ask_stream()`
- `src/chat.py` — new: `Chat` class
- `src/test_stream.py` — new: streaming test
- `src/test_chat.py` — new: conversation memory test

## Status: ✅ Chapter 3 complete, all code verified working