import os


def get_files_info(working_directory, directory="."):
    wdir_abs_path = os.path.abspath(working_directory)
    dir_abs_path = os.path.abspath(os.path.join(working_directory, directory))
    # CHECK: validate within working directory boundary
    if not dir_abs_path.startswith(wdir_abs_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # CHECK: validate if directory
    if not os.path.isdir(dir_abs_path):
        return f'Error: "{directory}" is not a directory'

    # CHECK: if directory or file actually exists

    contents = get_dir_contents(dir_abs_path)
    return contents


def get_dir_contents(dir_path):
    try:
        contents = os.listdir(dir_path)
        contents_info = []
        for item in contents:
            item_path = os.path.join(dir_path, item)
            size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            contents_info.append(
                f'- {item}: file_size={size} bytes, is_dir={is_dir}'
            )
        return '\n'.join(contents_info)
    except Exception as err:
        return f'Error: {err=}'
