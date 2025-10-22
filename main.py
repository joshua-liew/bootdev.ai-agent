import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function
from config import MAX_CALLS


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

    for _ in range(MAX_CALLS):
        try:
            result = generate_content(client, messages, verbose)
        except Exception as err:
            print(f"Exiting with code 1: {err=}")
            sys.exit(1)
        if result:
            print(f"Final response:\n{result}")
            break

    return sys.exit(0)


def generate_content(client, messages, verbose):
    """
    Return values: None | str
    By default, LLM calls a function, updates the messages & return None.
    Returns a string (response.text) when the action is not a function call.
    """
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

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("Fatal: no response from function call; Exiting.")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("Fatal: no function responses generated; Exiting.")

    # Update messages, mutating list outside of the function scope
    # NOTE: candidate.content is of type (Content)
    if not response.candidates:
        raise "Fatal: response does not contain 'candidates' property"
    for candidate in response.candidates:
        messages.append(candidate.content)
    # function_responses if a list of type (Parts)
    new_message = types.Content(
        role="user",
        parts=function_responses,
    )
    messages.append(new_message)

    return None


if __name__ == "__main__":
    main()
