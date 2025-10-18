import os
from .config import *


def get_file_content(working_directory, file_path):
    wdir_abs_path = os.path.abspath(working_directory)
    file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not file_abs_path.startswith(wdir_abs_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(file_abs_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(file_abs_path, "r") as f:
            file_content = f.read(FILE_CONTENT_MAX_SIZE)
            if len(file_content) == FILE_CONTENT_MAX_SIZE:
                file_content += (
                    f'[...File "{file_path}" truncated at {FILE_CONTENT_MAX_SIZE} characters]'
                )
            return file_content
    except Exception as err:
        return f'Error reading file "{filepath}": {err=}'
