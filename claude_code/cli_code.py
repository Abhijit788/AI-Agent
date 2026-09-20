from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
import os
import subprocess
import json


class ConversationMemory:

    def __init__(self, system_prompt):
        self.system_prompt = system_prompt
        self.messages = []

    def add(self, role, content):
        self.messages.append({
            "role": role,
            "content": content
        })

    def get_context(self):
        return [
            {
                "role": "system",
                "content": self.system_prompt
            },
            *self.messages
        ]
    


# --------------------------------------------------
# Configuration
# --------------------------------------------------

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in .env")


client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)


# --------------------------------------------------
# Tools
# --------------------------------------------------

def read_file(filename):
    try:
        file_path = Path(filename)

        if not file_path.exists():
            return {
                "success": False,
                "filename": filename,
                "error": "File does not exist."
            }

        content = file_path.read_text(encoding="utf-8")

        return {
            "success": True,
            "filename": filename,
            "content": content
        }

    except Exception as e:
        return {
            "success": False,
            "filename": filename,
            "error": str(e)
        }


def write_file(filename, content):
    try:
        file_path = Path(filename)

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        file_path.write_text(
            content,
            encoding="utf-8"
        )

        return {
            "success": True,
            "filename": str(file_path),
            "message": "File written successfully."
        }

    except Exception as e:
        return {
            "success": False,
            "filename": filename,
            "error": str(e)
        }


def run_command(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )

        return {
            "success": result.returncode == 0,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "return_code": -1,
            "stdout": "",
            "stderr": "Command timed out after 30 seconds."
        }

    except Exception as e:
        return {
            "success": False,
            "return_code": -1,
            "stdout": "",
            "stderr": str(e)
        }


# --------------------------------------------------
# Tool definitions sent to the model
# --------------------------------------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of an existing file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Path of the file to read."
                    }
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Create or overwrite a complete file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Path of the file to create."
                    },
                    "content": {
                        "type": "string",
                        "description": "Complete contents of the file."
                    }
                },
                "required": ["filename", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Run a PowerShell command on the local machine.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "PowerShell command to execute."
                    }
                },
                "required": ["command"]
            }
        }
    }
]


# --------------------------------------------------
# Map tool names to actual Python functions
# --------------------------------------------------

AVAILABLE_TOOLS = {
    "read_file": read_file,
    "write_file": write_file,
    "run_command": run_command
}


# --------------------------------------------------
# System prompt
# --------------------------------------------------

SYSTEM_PROMPT = """
You are a coding agent running on the user's local Windows machine.

Understand the user's request and use the available tools when necessary.

For coding tasks:
- Inspect existing files before modifying them when necessary.
- Create complete implementations, not placeholders.
- Use write_file to create or modify source files.
- Use read_file to inspect existing files.
- Use run_command to run programs, syntax checks, and tests.
- Verify your work before finishing.
- If a tool fails, inspect the error and recover when possible.
- Do not claim something was completed unless you have verified it.

write_file automatically creates missing parent directories.
Do not use run_command just to create a directory before writing files.

The user's operating system is Windows.
The user's shell is PowerShell.
"""


# --------------------------------------------------
# Agent
# --------------------------------------------------
memory = ConversationMemory(SYSTEM_PROMPT)

while True:

    user_input = input("👉 ")

    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    memory.add("user", user_input)

    while True:

        try:
            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=memory.get_context(),
                tools=TOOLS,
                tool_choice="auto",
            )

        except Exception as e:
            print("❌ Groq request failed:", e)
            break

        message = response.choices[0].message

        # ------------------------------------------
        # Model has finished
        # ------------------------------------------

        if not message.tool_calls:

            print("\n🤖", message.content)
            messages.append(message)
            break

        # ------------------------------------------
        # Store assistant tool-call message
        # ------------------------------------------

        messages.append(message)

        # ------------------------------------------
        # Execute tools
        # ------------------------------------------

        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            try:
                tool_input = json.loads(
                    tool_call.function.arguments
                )
            except json.JSONDecodeError as e:

                tool_result = {
                    "success": False,
                    "error": f"Invalid tool arguments: {e}"
                }

            else:

                if tool_name not in AVAILABLE_TOOLS:

                    tool_result = {
                        "success": False,
                        "error": f"Unknown tool: {tool_name}"
                    }

                else:

                    print(f"🔧 {tool_name}")

                    try:
                        tool_function = AVAILABLE_TOOLS[tool_name]

                        tool_result = tool_function(
                            **tool_input
                        )

                    except Exception as e:

                        tool_result = {
                            "success": False,
                            "error": str(e)
                        }

            # --------------------------------------
            # Send result back to model
            # --------------------------------------

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result)
            })

    else:

        print("❌ Agent stopped: maximum step limit reached.")