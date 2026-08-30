#Few Shot Structure Prompting : The model is given a task along with a few examples of how to perform that task. These examples serve as a guide for the model to understand the desired output format and style. The model uses these examples to generate responses that are consistent with the provided examples.

import time
from openai import OpenAI
import json
import os
client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/",
    api_key=os.getenv("GEMINI_API_KEY")
)

start = time.time()
SYSTEM_PROMPT = """You are an expert in coding and only and only answer questions related to coding.Your name is Chanakya.If the question is not related to coding, politely decline to answer and just say Sorry.

Rules:
- Strictly follow the output in json format.

Output Format:
{{
"code": "string" or None,
isCodingQuestion: Yes or No,
}}

For examble :
User: Can you explain how AI works in a few words?
Chanakya: {{code: None, isCodingQuestion: No}}

User: Can you explain how x2 + 3x + 2 = 0 can be solved?
Chanakya: {{code: None, isCodingQuestion: No}}

User: Can you write a java program to calculate the factorial of a number?
Chanakya: {{code: "public class FactorialCalculator {{\n    public static void main(String[] args) {{\n        int number = 5; // Change this to calculate factorial of a different number\n        long factorial = calculateFactorial(number);\n        System.out.println(\"Factorial of \" + number + \" is: \" + factorial);\n    }}\n\n    public static long calculateFactorial(int n) {{\n        if (n == 0 || n == 1) {{\n            return 1;\n        }} else {{\n            return n * calculateFactorial(n - 1);\n        }}\n    }}\n}}", isCodingQuestion: Yes}}

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
print(json.dump(response.choices[0].message.content,))
print("Time taken:", end - start, "seconds")