import os,re
import requests
from .download_path import construct_npath
import shutil
from .nHentaiScraper import *
import concurrent.futures

def download_page(arg):
    base_url, file_type, i, path_file, headers = arg
    if not os.path.exists(path_file):
        os.makedirs(os.path.dirname(path_file), exist_ok=True)
        r = requests.get(f"{base_url}{i}{file_type}", headers=headers)
        if r.status_code == 200:
            with open(path_file, "wb") as f:
                f.write(r.content)
            print(f"Page {i} Downloaded")
        else:
            print(f"Page {i} failed with status {r.status_code}")
    else:
        print(f"Page {i} already exists")
class downloadManager():
    
    saved_dir = os.path.dirname(os.path.abspath(__file__))
    def download_doujin(self, sauce):
        headers = {
        "Referer": "https://nhentai.net",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
        }
        results = fetch_doujin_src(sauce)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        name = get_name(sauce)
        pdf = name + ".pdf"
        target_folder = os.path.join(parent_dir, "Downloads", "Saved_Doujins", name, pdf)
        if os.path.exists(target_folder):
            print("Already exists a download of this doujin!")
            return 1
        pages = fetch_page_num(sauce)
        name = get_name(sauce)
        if results:
            args_list = []
            for i in range(1, pages + 1):
                file_name = f"Page_{i:03}{results[1]}"
                path_file = construct_npath([name, file_name])
                args_list.append((results[0], results[1], i, path_file, headers))

        with concurrent.futures.ThreadPoolExecutor(max_workers = 5) as executor:
            executor.map(download_page, args_list)
    
    def delete(self,doujin):
        doujin_name = get_name(doujin)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        doujin_folder = os.path.join(parent_dir, "Downloads", "Saved_Doujins",doujin_name)
        if os.path.exists(doujin_folder):
            shutil.rmtree(doujin_folder)
            print(f"Deleted manga folder: {doujin_folder}")
        else:
            print(f"Folder does not exist{doujin_folder}")


