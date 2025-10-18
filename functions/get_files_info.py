import os

def get_files_info(working_directory, directory="."):
    work_dir_path_abs = os.path.abspath(working_directory)
    user_dir_path_full = os.path.join(work_dir_path_abs, directory)
    user_dir_path_abs = os.path.abspath(user_dir_path_full)
    # CHECK: validate within working directory boundary
    if not work_dir_path_abs in user_dir_path_abs:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # CHECK: directory is a file
    if os.path.isfile(user_dir_path_abs):
        return f'Error: "{directory}" is not a directory'

    # CHECK: if directory or file actually exists

    return f'Success: path is {user_dir_path_abs}'
