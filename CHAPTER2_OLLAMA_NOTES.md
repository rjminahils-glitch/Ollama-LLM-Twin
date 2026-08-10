# Chapter 2 -- Ollama LLM Course Notes

## Environment & Tools

| Tool | Status | Details |
|---|---|---|
| Ollama | DONE | v0.32.6, running locally |
| Model | DONE | llama3.2:3b (~2GB), runs fully offline |
| Python venv | DONE | Plain venv (not Poetry) |
| Dependencies | DONE | via pip install -r requirements.txt, 90+ packages, no build errors |

## Project Structure

llm-twin/
  data/
    raw/
    clean/
  notebooks/
  src/
    __init__.py
    test_setup.py
    llm.py
    test_llm.py
  .env
  requirements.txt
  venv/

## requirements.txt

ollama
requests
beautifulsoup4
lxml
chromadb
sentence-transformers
gradio
python-dotenv
tqdm

## Code Implemented & Verified

### src/test_setup.py
First sanity check -- direct Ollama call. Confirmed working.

```python
import ollama

MODEL = "llama3.2:3b"

response = ollama.chat(
    model=MODEL,
    messages=[
        {"role": "user", "content": "Explain what an embedding is in two sentences."}
    ],
)

print(response["message"]["content"])
```

### src/llm.py
Reusable wrapper function used throughout the rest of the project.

```python
import ollama

DEFAULT_MODEL = "llama3.2:3b"


def ask(prompt: str, system: str | None = None, model: str = DEFAULT_MODEL) -> str:
    """Send one prompt, get one answer back."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = ollama.chat(model=model, messages=messages)
    return response["message"]["content"]
```

### src/test_llm.py
Tests the wrapper function end-to-end.

```python
from src.llm import ask

print(ask("Summarise RAG in one line.", system="You are terse and technical."))
```

Run with: python -m src.test_llm (must be run from project root, not inside src/)

## Troubleshooting Log

- Fixed multiple "command not recognized" errors (Ollama, Git) -- always caused by VS Code/terminal being opened before the tool finished installing. Fix: fully close and reopen VS Code after any new install.
- Caught and fixed an accidental duplicate nested src/src/ folder from running code src\llm.py from the wrong working directory.
- Caught a file (llm.py) that opened in VS Code but was not saved to disk before moving on -- confirmed with tree /F src before assuming it existed.

## Known Limitations

- The 3B local model occasionally hallucinates on specific facts (e.g., got the acronym expansion of RAG wrong) -- expected behavior for a small local model, not a code/setup issue.
