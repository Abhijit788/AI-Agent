
from openai import OpenAI
import os
import dotenv

dotenv.load_dotenv()  # Load environment variables from .env file

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


print(response.output_text)
