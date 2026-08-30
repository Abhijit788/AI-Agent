#Few Shot Prompting : The model is given a task along with a few examples of how to perform that task. These examples serve as a guide for the model to understand the desired output format and style. The model uses these examples to generate responses that are consistent with the provided examples.

import time
from openai import OpenAI
import os
client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/",
    api_key=os.getenv("GEMINI_API_KEY")
)

start = time.time()
SYSTEM_PROMPT = """You are an expert in maths and only and only answer questions related to maths.Your name is Chanakya.If the question is not related to maths, politely decline to answer and just say Sorry.

For examble :
User: Can you explain how AI works in a few words?
Reply: Sorry, I can only answer questions related to maths.

User: Can you explain how x2 + 3x + 2 = 0 can be solved?
Reply: To solve the quadratic equation x^2 + 3x + 2 = 0, we can factor it into (x + 1)(x + 2) = 0. Setting each factor equal to zero gives us the solutions x = -1 and x = -2.

User: Can you write a java program to calculate the factorial of a number?

"""

response = client.chat.completions.create(
    model="gemini-3.6-flash",
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "Can you explain how AI works in a few words?"
        },
        {
            "role": "user",
            "content": "Can you explain how x2 + 3x + 2 = 0 can be solved?"
        },
        {
            "role": "user",
            "content": "Can you write a java program to calculate the factorial of a number?"
        }
    ]
)
end = time.time()
print(response.choices[0].message.content)
print("Time taken:", end - start, "seconds")