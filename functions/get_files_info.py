import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'   Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'   Error: "{directory}" is not a directory'
    
        results = []
        for item in os.listdir(target_dir): 
            dir_help = os.path.normpath(os.path.join(target_dir, item))
            size = os.path.getsize(dir_help)
            is_dir = os.path.isdir(dir_help)
            combined = f'   - {item}: file_size={size} bytes, is_dir={is_dir}'
            results.append(combined)
        return "\n".join(results)
    except Exception as e:
        return f"   Error: {e}"
