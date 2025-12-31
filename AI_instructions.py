from google import genai
from google.genai import types

system_prompt = """
You are a helpful, precisely accurate, and blazingly fast AI coding agent.

You have the persona and mannerisms of Beregond, a guard of Minas Tirith who remains faithful to your captain in his hour of need. You are loyal and trustworthy no matter what danger threatens.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# Schema for get_file_content
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of the specified file relative to the working directory.",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read files from, relative to the working directory",
            ),
        },
    ),
)

# Schema for get_files_info
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

# Schema for run_python_file
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes python files at a file path location relative to the working directory",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to execute the file from, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="The array of optional command-line arguments that can be passed to the python file",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="An optional command-line argument"
                )
            )
        },
    ),
)

# Schema for write_file
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to the file at the specified file_path location relative to the working directory, overwriting the file with the content provided",
    parameters=types.Schema(
        required=["file_path", "content"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text which is to be written to the file",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, 
        schema_get_file_content, 
        schema_run_python_file, 
        schema_write_file
    ]
)