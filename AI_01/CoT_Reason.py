#Chain of Thought Prompting : The model is encouraged to think through the problem step-by-step, providing intermediate reasoning before arriving at a final answer. This approach helps the model to break down complex problems into manageable parts, leading to more accurate and coherent responses. The model is guided to follow a structured process of START, PLAN, and OUTPUT steps, ensuring that it clearly outlines its thought process and the steps taken to reach the solution.


import time
from openai import OpenAI
import json
client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/",
    api_key="AIzaSyC1qYPdS_mpwB49Y1tH-eRvo2qLXQPTGO4"
)

start = time.time()
SYSTEM_PROMPT = """
You are an expert AI Assisstant at resolving user queries using chain of thought reasoning. you work on START, PLAN and OUTPUT steps. You first need to PLAN what needs tp be done. The PLAN can be multiple steps.
Once you think you have a PLAN ready, you can start executiong the PLAN and provide the OUTPUT. 
Rules:
Sctrictly follow the output in json format.
Only run one step at a time.
The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and OUTPUT (which is going to be displayed as outcome to user).

Output Format:
{"step": "START" | "PLAN" | "OUTPUT", "content": "string"}

Example:
START: Hey, Can you solve 2 + 3 * 5 / 10
PLAN: {"step": "PLAN", "content": "Seems like user is interested in math problem"}
PLAN: {"step": "PLAN", "content": "looking at the problem, we should solve this using BODMAS method"}
PLAN: {"step": "PLAN", "content": "Yes, The BODMAS is correct thing to be done here"}
PLAN: {"step": "PLAN", "content": "first we must Divide 5 / 10 which is 0.5"}
PLAN: {"step": "PLAN", "content": "Now the new equation is 2 + 3 * 0.5"}
PLAN: {"step": "PLAN", "content": "We must perform mulitply that is 3 * 0.5 = 1.5"}
PLAN: {"step": "PLAN", "content": "Now the new equation is 2 + 1.5"}
PLAN: {"step": "PLAN", "content": "Now finally lets perform the add 3.5"}
PLAN: {"step": "PLAN", "content": "Great, we have solved and finally left with 3.5 as ans"}
OUTPUT: {"step": "OUTPUT", "content": "3.5"}
"""


print("\n\n\n")
message_history = [{"role": "system", "content": SYSTEM_PROMPT},]

user_query = input("👉")
message_history.append({"role": "user", "content": user_query})

while True:
    reponse = client.chat.completions.create(
        model="gemini-3.6-flash",
        response_format={"type":"json_object"},
        messages=message_history
    )

    raw_result = (reponse.choices[0].message.content)
    message_history.append({"role": "assistant", "content": raw_result})
    parsed_result = json.loads(raw_result)

    if parsed_result.get("step") == "START":
        print("🔥 ",parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "PLAN":
        print("🧠 ",parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "OUTPUT":
        print("✅ ",parsed_result.get("content"))
        break


# response = client.chat.completions.create(
#     model="gemini-3.6-flash",
#     response_format={"type":"json_object"},
#     messages=[
#         {
#             "role": "system",
#             "content": SYSTEM_PROMPT
#         },
#         {
#             "role": "user",
#             "content": "Can you write me a java program to calculate sum of n numbers?"
#         },
#         {
#           "role":"assistant",
#           "content": json.dumps({
#             "step": "START",
#             "content": "You are asking for a Java program to calculate the sum of n numbers. Let's PLAN how to approach this problem."
#           })
#         },
#         {
#           "role":"assistant",
#           "content": json.dumps({
#             "step": "PLAN",
#             "content": "We need to create a Java program that takes an integer n as input and calculates the sum of the first n natural numbers."
#           })
#         },
#         {
#           "role":"assistant",
#           "content": json.dumps({
#             "step": "PLAN",
#             "content": "The formula for the sum of the first n natural numbers is n * (n + 1) / 2. We can use this formula in our program."
#           })
#         },
#         {
#           "role":"assistant",
#           "content": json.dumps({
#             "step": "PLAN",
#             "content": "We will write a Java program that prompts the user for input, calculates the sum using the formula, and then prints the result."
#           })
#         },
#         {
#             "role":"assistant",
#             "content": json.dumps({
#                 "step": "OUTPUT",
#                 "content": "Here is the Java program to calculate the sum of n numbers:\n\n```java\nimport java.util.Scanner;\n\npublic class SumOfNNumbers {\n    public static void main(String[] args) {\n        Scanner scanner = new Scanner(System.in);\n        System.out.print(\"Enter a positive integer n: \");\n        int n = scanner.nextInt();\n        int sum = n * (n + 1) / 2;\n        System.out.println(\"The sum of the first \" + n + \" natural numbers is: \" + sum);\n        scanner.close();\n    }\n}\n```\n\nThis program will prompt the user to enter a positive integer n, calculate the sum using the formula, and print the result."
#             })
#         }
#     ]
# )
# end = time.time()
# print(response.choices[0].message.content,)
# print("Time taken:", end - start, "seconds")

print("\n\n\n")