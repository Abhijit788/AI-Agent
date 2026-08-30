from google import genai
import time
import os

client = genai.Client(
  api_key=os.getenv("GEMINI_API_KEY")
)
start = time.time()
interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input="Explain how AI works in a few words"
)
end = time.time()
print(interaction.output_text)
print("Time taken:", end - start, "seconds")