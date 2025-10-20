import os
import subprocess


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

    TIMEOUT = 30
    CAPTURE_OUTPUT = True
    CWD = os.path.dirname(file_abs_path)
    PYFILE = os.path.basename(file_abs_path)
    ARGS = args.append(PYFILE)
    try:
        completed_ps = subprocess.run(
            args=ARGS,
            capture_output=CAPTURE_OUTPUT,
            cwd=CWD,
            timeout=TIMEOUT,
        )
    except Exception as err:
        return f'Error: executing Python file: {err=}'

    result = f'STDOUT: {completed_ps.stdout}\nSTDERR: {completed_ps.stderr}'
    if completed_ps.returncode != 0:
        result += f'\nProcess exited with code {completed_ps.returncode}'
    if not completed_ps.stdout:
        result += f'\nNo output produced'
    return result
