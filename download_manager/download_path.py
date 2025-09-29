import os
import re

def construct_npath(paths, base_folder="Saved_Doujins",folder_max_len=75):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    target_folder = os.path.join(parent_dir, "Downloads", base_folder)
    os.makedirs(target_folder, exist_ok=True)

    folder_name = paths[0][:folder_max_len].replace("/", "_").replace("\\", "_").replace(":", "_").replace("|", "_")
    folder_path = os.path.join(target_folder, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    file_name = paths[-1].replace("/", "_").replace("\\", "_").replace(":", "_").replace("|", "_")

    return os.path.join(folder_path, file_name)

def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', "_", name)