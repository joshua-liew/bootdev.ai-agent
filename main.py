import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    args = sys.argv
    if "--verbose" in args:
        i = args.index("--verbose")
        args = args[:i] + args[i+1:] # take option out

    NUM_OF_ARGS = 2
    if len(args) < NUM_OF_ARGS:
        print("Usage: main.py [prompt]")
        print(f"Error: expected {NUM_OF_ARGS} arguments; received {len(args)} - exiting with code 1")
        exit(1)
    user_prompt = str(sys.argv[1])

    print("Hello from ai-agent!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # Store roles
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=user_prompt)]
        ),
    ]

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages
    )
    print(response.text)

    print(f"User prompt: {user_prompt}")
    # Print token info
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
