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

    iter, stop_iter = (0, False)
    while (iter < MAX_CALLS and not stop_iter):
        try:
            response_text, candidates, function_responses \
                = generate_content(client, messages, verbose)
        except Exception as err:
            print(f"Exiting with code 1: {err=}")
            sys.exit(1)

        if response_text is not None:
            print(f"Final response:\n{response_text}")
            stop_iter = True
        # Update messages to pass into LLM
        if (candidates is not None) and (function_responses is not None):
            for candidate in candidates:
                messages.append(candidate.content)
            messages.append(
                types.Content(
                    role="user",
                    parts=function_responses,
                )
            )
            iter += 1

    if (iter == MAX_CALLS) and not stop_iter:
        print(f"Exiting with code 1: could not complete task within max ({MAX_CALLS}) iterations .")
        return sys.exit(1)

    return sys.exit(0)


def generate_content(client, messages, verbose):
    """
    Return values: (response.text, response.candidates, function_responses)
    Returns a tuple with the following 2 possible permutations of values
    - (response.text, None, None) : LLM does not call a function
    - (None, response.candidates, function_responses) : LLM calls a function
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
        return (response.text, None, None)

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

    if not response.candidates:
        raise Exception("Fatal: no property 'candidates' in response; Exiting.")
    if not function_responses:
        raise Exception("Fatal: no function responses generated; Exiting.")
    return (None, response.candidates, function_responses)


if __name__ == "__main__":
    main()
