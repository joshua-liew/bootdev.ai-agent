import os

def get_files_info(working_directory, directory="."):
    work_dir_path_abs = os.path.abspath(working_directory)
    user_dir_path_full = os.path.join(work_dir_path_abs, directory)
    user_dir_path_abs = os.path.abspath(user_dir_path_full)
    if not work_dir_path_abs in user_dir_path_abs:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    print("work_dir_path_abs:", work_dir_path_abs)
    print("user_dir_path_full:", user_dir_path_full)
    print("user_dir_path_abs:", user_dir_path_abs)
    return f'Success'
