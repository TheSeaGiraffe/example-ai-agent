import argparse
import os
from argparse import Namespace

from dotenv import load_dotenv
from google import genai
from google.genai.types import Content, Part


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
    messages = [Content(role="user", parts=[Part(text=user_prompt)])]
    response = client.models.generate_content(model=model, contents=messages)

    if args.verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {verbose_token_count(user_prompt)}")
        print(f"Response tokens: {verbose_token_count(response.text)}\n")

    print("Response:")
    print(f"\n{response.text}")


if __name__ == "__main__":
    main()
