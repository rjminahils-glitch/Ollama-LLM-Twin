import ollama

MODEL = "llama3.2:3b"

response = ollama.chat(
    model=MODEL,
    messages=[
        {"role": "user", "content": "Explain what an embedding is in two sentences."}
    ],
)

print(response["message"]["content"])