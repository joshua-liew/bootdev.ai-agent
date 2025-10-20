import os


def write_file(working_directory, file_path, content):
    wdir_abs_path = os.path.abspath(working_directory)
    file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    # CHECK: validate within working directory boundary
    if not file_abs_path.startswith(wdir_abs_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    file_rel_path = os.path.join(working_directory, file_path)
    if not os.path.isfile(file_abs_path):
        try:
            open(file_rel_path, 'x')
        except Exception as err:
            return f'Error: cannot create file "{file_rel_path}"; {err=}'

    try:
        with open(file_abs_path, 'w') as f:
            f.write(content)
    except Exception as err:
        return f'Error: could not write to file "{file_rel_path}"; {err=}'

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
