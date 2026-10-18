import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args:
            command.extend(args)

        result = subprocess.run(command, cwd=working_dir_abs, capture_output=True, timeout=30, text=True)
        
        messages = []
        if result.returncode != 0:
            messages.append(f"Process exited with code {result.returncode}")
        if result.stdout == "" and result.stderr == "":
            messages.append("No output produced")
        if result.stdout != "":
            messages.append(f"STDOUT: {result.stdout}")
        if result.stderr != "":
            messages.append(f"STDERR:{result.stderr}")
            
        return "\n".join(messages)

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs python file relative to the working directory with optional list of string arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                        },
                    "description": "List of optional string arguments"
                },
            },
            "required": ["file_path"],
        },
    },
}
