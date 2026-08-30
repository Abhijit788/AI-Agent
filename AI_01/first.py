from openai import OpenAI
import time
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

while True:
    prompt = input("\nYou: ")
    start = time.time()
    if prompt.lower() == "exit":
        break

    response = client.chat.completions.create(
        model="qwen3:0.6b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print("\nAI:", response.choices[0].message.content)
    end = time.time()
    print("Time taken:", end - start, "seconds")
