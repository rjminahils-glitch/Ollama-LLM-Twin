from src.chat import Chat

chat = Chat(system="You are a concise ML tutor.")
print(chat.send("What is a vector database?"))
print(chat.send("How is it different from Postgres?"))  # 'it' should resolve correctly