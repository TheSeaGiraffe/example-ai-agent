import argparse
import os
from argparse import Namespace

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.types import Content, Part

import functions.function_declarations as funcdecs

available_functions = types.Tool(
    function_declarations=[
        funcdecs.schema_get_files_info,
        funcdecs.schema_get_file_content,
        funcdecs.schema_run_python_file,
        funcdecs.schema_write_file,
    ]
)


def parse_args() -> Namespace:
    parser = argparse.ArgumentParser(
        prog="example_ai_agent",
        description="Example AI agent created as part of the Boot.dev backend path",
    )
    parser.add_argument("prompt", nargs="+", type=str, help="Prompt to the AI agent")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    return parser.parse_args()


def verbose_token_count(text: str) -> int:
    return len(text.replace(" ", "")) // 4


def main():
    # Parse command line args
    args = parse_args()

    # Init model
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # Generate content using model
    model = "gemini-2.0-flash-001"
    user_prompt = " ".join(args.prompt)
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    messages = [Content(role="user", parts=[Part(text=user_prompt)])]
    response = client.models.generate_content(
        model=model,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if args.verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {verbose_token_count(user_prompt)}")
        print(f"Response tokens: {verbose_token_count(response.text)}\n")

    # print("Response:")
    function_calls = response.function_calls
    if function_calls:
        for function_call in function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f"Response: {response.text}")


if __name__ == "__main__":
    main()
