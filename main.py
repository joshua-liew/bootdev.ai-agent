import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt, available_functions


def main():
    args = []
    verbose = "--verbose" in sys.argv
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    REQUIRED_ARGS = 1
    if not args or (len(args) < REQUIRED_ARGS or len(args) > REQUIRED_ARGS):
        print("AI Code Assistant")
        print("=================")
        print("Usage: main.py <PROMPT> [--verbose]")
        print(f"Error: expected {REQUIRED_ARGS} arguments; received {len(args)} - exiting with code 1")
        exit(1)
    user_prompt = str(args[0])

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if verbose:
        print(f"User prompt: {user_prompt}")

    # Store roles
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=user_prompt)]
        ),
    ]

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
        ),
    )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:")
    if response.function_calls:
        for func in response.function_calls:
            print(f"Calling function: {func.name}({func.args})")
    print(response.text)


if __name__ == "__main__":
    main()
