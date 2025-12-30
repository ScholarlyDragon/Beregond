import os
import subprocess

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
        
        # Subprocess for running the file:
        command = ["python", file_abs]
        if args:
            command.extend(args)
        result = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
        output_list = []
        if result.returncode != 0:
            output_list.append(f"Process exited with code {result.returncode}")
        if not result.stderr and not result.stdout:
            output_list.append("No output produced")
        else:
            if result.stdout:
                output_list.append(f"STDOUT: {result.stdout}")
            if result.stderr:
                output_list.append(f"STDERR: {result.stderr}")
        output = "\n".join(output_list)
        return output
    
    except Exception as e:
        return f"Error: executing Python file: {e}"