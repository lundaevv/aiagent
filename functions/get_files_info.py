import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        if directory == ".":
            directory = "current" 
        
        is_in_permitted_scope_target_dir: bool = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not is_in_permitted_scope_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory\n'
        
        is_dir_target_dir: bool = os.path.isdir(target_dir)
        if not is_dir_target_dir:
            return f'Error: "{directory}" is not a directory\n'

        target_dir_items: list[str] = os.listdir(target_dir)

        return_str = ""
        for item in target_dir_items:
            name = str(item)
            if name[0] == "_":
                continue
            path = os.path.normpath(os.path.join(target_dir, name))
            file_size = os.path.getsize(path)
            is_dir = os.path.isdir(path)
            return_str += f"- {name}: file_size={file_size} bytes, is_dir={is_dir}\n"

        return return_str
    except Exception as e:
        return f"Error: {e}\n"