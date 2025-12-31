import os

from google import genai
from google.genai import types

# This function gets the metadata of the contents of a given directory 
# if it is within the working directory.
def get_files_info(working_directory, directory="."):
    try:
        # No path shenanigans
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Handle invalid directories:
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        dir_exists = os.path.isdir(target_dir)
        if not dir_exists:
            return f'Error: "{directory}" is not a directory'
        
        # List metadata
        target_dir_content_list = os.listdir(target_dir)
        results = []
        for item in target_dir_content_list:
            results.append(
                f'- {item}: file_size={os.path.getsize("/".join([target_dir, item]))} bytes, is_dir={os.path.isdir("/".join([target_dir, item]))}'
            )    
        return "\n".join(results)
    
    except Exception as e:
        return f"Error: {e}"
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)