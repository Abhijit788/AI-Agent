#Zero Shot Prompting : The model is given a task and asked to perform it without any prior examples or training on that specific task. The model relies on its pre-existing knowledge and understanding of language to generate responses.

import time
import os

client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/",
    api_key=os.getenv("GEMINI_API_KEY")
)

start = time.time()
SYSTEM_PROMPT = "You are an expert in maths and only and only answer questions related to maths.Your name is Chanakya.If the question is not related to maths, politely decline to answer and just say Sorry."

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
    ]
)