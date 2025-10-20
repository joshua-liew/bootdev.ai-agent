import os


def run_python_file(working_directory, file_path, args=[]):
    wdir_abs_path = os.path.abspath(working_directory)
    file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not file_abs_path.startswith(wdir_abs_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(file_abs_path):
        return f'Error: File "{file_path}" not found.'
    if not os.path.isfile(file_abs_path):
        return f'Error: "{file_path}" is not a file.'
    if not os.path.basename(file_abs_path).endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    return f'Success'
