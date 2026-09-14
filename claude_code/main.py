# main.py

# This is a minimal example of using the OpenAI Python library.
# Make sure you have the `openai` package installed:
#   pip install openai
# And set your OpenAI API key via the environment variable OPENAI_API_KEY
#   or by setting it directly in the script.

import os
from openai import OpenAI

# Optionally set the API key in the script. Replace "YOUR_API_KEY" with your key.
# os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

# Create a client instance.
client = OpenAI()

# Define a simple prompt.
prompt = "Translate the following English text to French: 'Hello, world!'
"

# Perform a completion request.
try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or any model you have access to
        messages=[{"role": "user", "content": prompt}],
        max_tokens=60,
        temperature=0.5,
    )
    print("Response:")
    print(response.choices[0].message.content.strip())
except Exception as e:
    print("Error during OpenAI request:", e)

