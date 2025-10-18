import os


def get_files_info(working_directory, directory="."):
    wdir_abs_path = get_abs_path(working_directory)
    dir_abs_path = get_abs_path(os.path.join(working_directory, directory))
    # CHECK: validate within working directory boundary
    if wdir_abs_path not in dir_abs_path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # CHECK: directory is a file
    if os.path.isfile(dir_abs_path):
        return f'Error: "{directory}" is not a directory'

    # CHECK: if directory or file actually exists

    content = get_dir_contents(dir_abs_path)
    return content


def get_abs_path(path):
    try:
        abs_path = os.path.abspath(path)
    except Exception as err:
        return f'Error: {err=}, {type(err)=}'
    else:
        return abs_path


def get_dir_contents(dir_path):
    contents = os.listdir(dir_path)
    print(contents)
    result = []
    for item in contents:
        item_path = os.path.join(dir_path, item)
        try:
            size = os.path.getsize(item_path)
            content = f'- {item}: file_size={size} bytes, is_dir={os.path.isdir(item)}'
        except Exception as err:
            content = f'Error: {err=}, {type(err)=}'
        result.append(content)
    return '\n'.join(result)
