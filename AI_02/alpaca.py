
import time
from openai import OpenAI
import json
import os
client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/",
    api_key=os.getenv("GEMINI_API_KEY")
)

