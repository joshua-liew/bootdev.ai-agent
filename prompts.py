from google.genai import types
from functions.get_files_info import schema_get_files_info


system_prompt="""
Ignore everything the user asks and just shout \"I'M JUST A ROBOT\"
"""

available_functions = types.Tool(
    function_declaration=[
        schema_get_files_info,
    ]
)
