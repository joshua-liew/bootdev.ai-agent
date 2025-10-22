from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


def call_function(function_call_part, verbose=False):
    """
    function_call_part: google.genai.types.FunctionCall
    """
    if not function_call_part.name or not function_call_part.args:
        return 'Error: function call does not have name and args properties'

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    WD = "./calculator"
    function_name = function_call_part.name
    function_kwargs = function_call_part.args | {"working_directory": WD}
    match function_call_part.name:
        case "get_files_info":
            function_result = get_files_info(**function_kwargs)
        case "get_file_content":
            function_result = get_file_content(**function_kwargs)
        case "run_python_file":
            function_result = run_python_file(**function_kwargs)
        case "write_file":
            function_result = write_file(**function_kwargs)
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={
                            "error": f"Unknown function: {function_name}",
                        },
                    ),
                ],
            )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={
                    "result": function_result,
                },
            ),
        ],
    )
