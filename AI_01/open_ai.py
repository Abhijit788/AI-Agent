from openai import OpenAI
import time

client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/",
    api_key="AIzaSyC1qYPdS_mpwB49Y1tH-eRvo2qLXQPTGO4"
)
start = time.time()
SYSTEM_PROMPT ="You are an expert in maths and only and only answer questions related to maths.Your name is Chanakya.If the question is not related to maths, politely decline to answer and just say Sorry."
reponse = client.chat.completions.create(
    model="gemini-3.6-flash",
    messages=[
      {
            "role": "system",
            "content": SYSTEM_PROMPT
      },
        { 
            "role": "user",
            "content": "Hi, I am Abhijit. How are you doing today?"
        },
        {
          "role": "user",
          "content": "Can you explain how AI works in a few words?"
        },
        {
          "role":"user",
          "content":"Can you explain how x2 + 3x + 2 = 0 can be solved?"
        }
    ]
)
end = time.time()
print(reponse.choices[0].message.content)
print("Time taken:", end - start, "seconds")