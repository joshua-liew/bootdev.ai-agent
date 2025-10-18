import os

def get_files_info(working_directory, directory="."):
    wdir_abs_path = get_abs_path(working_directory)
    dir_abs_path = get_abs_path(directory)
    # CHECK: validate within working directory boundary
    if not wdir_abs_path in dir_abs_path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # CHECK: directory is a file
    if os.path.isfile(dir_abs_path):
        return f'Error: "{directory}" is not a directory'

    # CHECK: if directory or file actually exists

    user_dir_content_list = os.listdir(dir_abs_path)
    user_dir_content_info = list(map(
        lambda item: f'- {item}: file_size={os.path.getsize(item)} bytes, is_dir={os.path.isdir(item)}',
        user_dir_content_list
    ))
    return "\n".join(user_dir_content_info)


def get_abs_path(path):
    try:
        abs_path = os.path.abspath(path)
    except Exception as err:
        return f'Error: {err=}, {type(err)=}'
    else:
        return abs_path
