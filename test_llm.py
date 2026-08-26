import ollama

response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "user",
            "content": "Explain what a logistics customer support AI agent does in one sentence."
        }
    ]
)

print(response["message"]["content"])