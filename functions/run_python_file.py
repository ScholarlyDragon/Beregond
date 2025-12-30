import os

def run_python_file(working_directory, file_path, args=None):
    try:
        # No path shenanigans:
        working_dir_abs = os.path.abspath(working_directory)
        file_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Handle invalid files:
        valid_target_file = os.path.commonpath([working_dir_abs, file_abs]) == working_dir_abs
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        file_exists = os.path.isfile(file_abs)
        if not file_exists:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", absolute_file_path]

    except Exception as e:
        return f"Error: {e}"