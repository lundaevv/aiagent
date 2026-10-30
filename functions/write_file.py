import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writing content into a specified file path relative to the working directory, providing a message if file is written or not",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to write content into, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write into the specified file"
                },
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
        parent_dir_abs = os.path.abspath(os.path.dirname(target_file_abs))

        is_in_permitted_scope: bool = os.path.commonpath([working_dir_abs, target_file_abs]) == working_dir_abs
        if not is_in_permitted_scope:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory\n'
        
        is_dir: bool = os.path.isdir(target_file_abs)
        if is_dir:
            return f'Error: Cannot write to "{file_path}" as it is a directory\n'

        os.makedirs(parent_dir_abs, exist_ok=True)

        with open(target_file_abs, "w") as f:
            written = f.write(content)
            if written == len(content):
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)\n'
            return f'Error: {len(content)} characters NOT written to "{file_path}"\n'
    
    except Exception as e:
        return f"Error: {e}\n"