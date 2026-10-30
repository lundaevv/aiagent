import os
from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Get content of the file in a specified file path relative to the working directory, providing file content as a str and truncating it with the message if the file is longer than MAX_CHARS",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to get content from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))

        is_in_permitted_scope: bool = os.path.commonpath([working_dir_abs, target_file_abs]) == working_dir_abs
        if not is_in_permitted_scope:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory\n'
        
        is_file: bool = os.path.isfile(target_file_abs)
        if not is_file:
            return f'Error: File not found or is not a regular file: "{file_path}"\n'

        with open(target_file_abs, "r") as f:
            file_content_string: str = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content_string

    except Exception as e:
        return f"Error: {e}\n"