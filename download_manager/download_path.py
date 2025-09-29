import os
import re

def construct_npath(paths,base_folder= "Saved_Doujins"):
    script_dir = os.path.dirname(os.path.abspath(__file__))

    parent_dir = os.path.dirname(script_dir)
    target_folder = os.path.join(parent_dir, "Downloads", base_folder)
    os.makedirs(target_folder, exist_ok=True)

    work_paths = paths.copy()
    result = target_folder

    while work_paths:
        result = os.path.join(result, length_check(work_paths.pop(0).replace("/", "_")))
    return result

def length_check(path_elem):
    result = ""
    BYTE_LENGTH_LIMIT = 255
    CODEC = "utf-8"
    byte_length = len(path_elem.encode(CODEC))
    if byte_length > BYTE_LENGTH_LIMIT:
        i = BYTE_LENGTH_LIMIT
        while not result:
            try:
                result = path_elem.encode(CODEC)[:i].decode(CODEC)
            except UnicodeDecodeError:
                i = i - 1
                continue
    else:
        result = path_elem
    return result
def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', "_", name)