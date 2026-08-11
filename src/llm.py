import ollama

DEFAULT_MODEL = "llama3.2:3b"

def ask(
    prompt: str,
    system: str | None = None,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    num_predict: int = 500,
) -> str:
    """Send one prompt, get one answer back."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = ollama.chat(
        model=model,
        messages=messages,
        options={
            "temperature": temperature,
            "top_p": top_p,
            "num_predict": num_predict,
        },
    )
    return response["message"]["content"]


def ask_stream(prompt: str, system: str | None = None, model: str = DEFAULT_MODEL):
    """Same as ask(), but prints the reply as it's generated."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    for chunk in ollama.chat(model=model, messages=messages, stream=True):
        print(chunk["message"]["content"], end="", flush=True)
    print()