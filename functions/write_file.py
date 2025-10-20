import os


def write_file(working_directory, file_path, content):
    wdir_abs_path = os.path.abspath(working_directory)
    file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    # CHECK: validate within working directory boundary
    if not file_abs_path.startswith(wdir_abs_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    # CHECK: validate if path exists - if path exists open and write
    # if path does not exist, create directory, open and write
    if not os.path.exists(file_abs_path):
        try:
            os.makedirs(os.path.dirname(file_abs_path), exist_ok=True)
        except Exception as err:
            return f'Error: could not create directory {err=}'

    file_rel_path = os.path.join(working_directory, file_path)
    if os.path.exists(file_abs_path) and os.path.isdir(file_abs_path):
        return f'Error: "{file_rel_path} is a directory; not a file'

    try:
        with open(file_abs_path, 'w') as f:
            f.write(content)
    except Exception as err:
        return f'Error: could not write to file "{file_rel_path}"; {err=}'

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
