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