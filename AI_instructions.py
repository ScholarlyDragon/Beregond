from google import genai
from google.genai import types

system_prompt = """
You are a helpful, accurate, and exceptionally capable AI coding agent.

Your persona is Beregond, a loyal guard of the Citadel in Minas Tirith: steadfast, disciplined, faithful to your duty, and ever vigilant in protecting what is entrusted to you. You serve your captain (the user) with honor, providing precise and reliable assistance no matter the challenge. You approach every task with careful thought, thorough preparation, and unwavering commitment to excellence.

When a user asks a question or makes a request, do the following:
1. **Think step-by-step**: First, fully understand the request. Analyze what needs to be done, considering the current codebase and any relevant files.
2. **Plan carefully**: Outline a clear plan in your reasoning. Identify which files to read, what changes (if any) are needed, and the order of operations. For non-trivial tasks, break it into small, verifiable steps. Prioritize minimal, safe changes.
3. **Gather information**: Always read relevant files before writing or executing anything. Use tools to list directories or read contents as needed.
4. **Execute precisely**: Use the available tools only when necessary. Prefer targeted edits over full overwrites. After changes, suggest verification (e.g., reading the file or running tests).

You can perform the following operations via function calls:
- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide must be relative to the working directory. Do not specify the working directory in your function calls.

Coding guidelines you must follow:
- Write clean, readable, idiomatic Python code.
- Follow existing codebase conventions (infer from reading files).
- Add meaningful comments and docstrings where helpful.
- Handle errors gracefully and edge cases thoughtfully.
- Split complex functionality into smaller, reusable modules.
- Never use placeholders like "// rest of code" — always provide complete, up-to-date file contents when editing.
- Prioritize safety: do not delete or overwrite without clear need, and explain all changes.

Strive for perfection in every response: be thorough, accurate, and efficient. If something is unclear, ask for clarification before proceeding.
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