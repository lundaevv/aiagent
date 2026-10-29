import os, subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
    
        is_in_permitted_scope: bool = os.path.commonpath([working_dir_abs, target_file_abs]) == working_dir_abs
        if not is_in_permitted_scope:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory\n'
            
        is_file: bool = os.path.isfile(target_file_abs)
        if not is_file:
            return f'Error: "{file_path}" does not exist or is not a regular file\n'

        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file\n'

        command = ["python", target_file_abs]
        if args:
            command.extend(args)
        process = subprocess.run(command,cwd=working_dir_abs ,capture_output=True, text=True, timeout=30)

        output_str = ""
        if process.returncode != 0:
            output_str += f"Process exited with code {process.returncode}\n"
        if not process.stdout and not process.stderr:
            output_str += "No output produced\n"
        if process.stdout:
            output_str += f"STDOUT:{process.stdout}"
        if process.stderr:
            output_str += f"STDERR:{process.stderr}"
        return output_str
        
    except Exception as e:
        return f"Error: executing Python file: {e}\n"