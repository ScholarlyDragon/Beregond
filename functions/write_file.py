import os

def write_file(working_directory, file_path, content):
    try:
        # No path shenanigans:
        working_dir_abs = os.path.abspath(working_directory)
        file_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Handle invalid files:
        valid_target_file = os.path.commonpath([working_dir_abs, file_abs]) == working_dir_abs
        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        dir_exists = os.path.isdir(file_abs)
        if dir_exists:
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        # Ensure parent directories exist:
        parent_dir = os.path.dirname(file_abs)
        os.makedirs(parent_dir, exist_ok=True)

        # Overwrite file contents:
        with open(file_abs, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"