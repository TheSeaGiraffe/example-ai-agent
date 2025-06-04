import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai.types import Content, Part

# Get prompt from command line
if len(sys.argv) == 1:
    print("Missing prompt to LLM.")
    sys.exit(1)

user_prompt = " ".join(sys.argv[1:])

# Init model
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Generate content using model
model = "gemini-2.0-flash-001"
messages = [Content(role="user", parts=[Part(text=user_prompt)])]
response = client.models.generate_content(model=model, contents=messages)

print(f"Prompt to {model} model:")
print(f"\n{user_prompt}")
print("\nResponse:")
print(f"\n{response.text}")
