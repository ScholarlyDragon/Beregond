import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        # No path shenanigans
        working_dir_abs = os.path.abspath(working_directory)
        file_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Handle invalid files:
        valid_target_file = os.path.commonpath([working_dir_abs, file_abs]) == working_dir_abs
        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        file_exists = os.path.isfile(file_abs)
        if not file_exists:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Read the file and return its contents as a string:
        with open(file_abs, "r") as f:
            content = f.read(MAX_CHARS)
            # Check if the file was bigger than MAX_CHARS:
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content

    except Exception as e:
        return f"Error: {e}"