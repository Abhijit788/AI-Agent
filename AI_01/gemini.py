from google import genai
import time

client = genai.Client(
  api_key="AIzaSyC1qYPdS_mpwB49Y1tH-eRvo2qLXQPTGO4"
)
start = time.time()
interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input="Explain how AI works in a few words"
)
end = time.time()
print(interaction.output_text)
print("Time taken:", end - start, "seconds")