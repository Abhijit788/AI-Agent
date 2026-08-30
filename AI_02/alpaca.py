
import time
from openai import OpenAI
import json
from venv import gemini_api_key
client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/",
    api_key=gemini_api_key
)

