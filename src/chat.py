import ollama
from src.llm import DEFAULT_MODEL


class Chat:
    """Holds conversation history and resends it each turn."""

    def __init__(self, system: str | None = None, model: str = DEFAULT_MODEL):
        self.model = model
        self.messages = []
        if system:
            self.messages.append({"role": "system", "content": system})

    def send(self, prompt: str, temperature: float = 0.7) -> str:
        self.messages.append({"role": "user", "content": prompt})

        response = ollama.chat(
            model=self.model,
            messages=self.messages,
            options={"temperature": temperature},
        )
        reply = response["message"]["content"]

        self.messages.append({"role": "assistant", "content": reply})
        return reply

    def reset(self):
        self.messages = self.messages[:1] if self.messages else []