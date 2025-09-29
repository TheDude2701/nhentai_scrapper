import os,re
import requests
from .download_path import construct_npath
import shutil
from .nHentaiScraper import *
import concurrent.futures
from .pdfconvert import images_to_pdf
from .download_path import sanitize_filename

def download_page(arg):
    base_url, i, path_file, headers = arg
    if not os.path.exists(path_file):
        os.makedirs(os.path.dirname(path_file), exist_ok=True)
        try:
            r = requests.get(base_url, headers=headers, timeout=15)
            r.raise_for_status()  
            with open(path_file, "wb") as f:
                f.write(r.content)
            print(f"Page {i} Downloaded")
        except requests.RequestException as e:
            print(f"Page {i} failed: {e}")

class downloadManager():
    
    saved_dir = os.path.dirname(os.path.abspath(__file__))
    def download_doujin(self, sauce, pdf = False):
        headers = {
        "Referer": "https://nhentai.net",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
        }
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        name = get_name(sauce)
        name_safe = sanitize_filename(name)[:75]
        folder_path = os.path.join(parent_dir, "Downloads", "Saved_Doujins", name_safe)
        os.makedirs(folder_path, exist_ok=True)
        pdf_file = os.path.join(folder_path, f"{name_safe}.pdf")
        if os.path.exists(pdf_file):
            print("Already exists a download of this doujin!")
            return 1
        pages = fetch_page_num(sauce)
        results = fetch_doujin_src(sauce,pages)
        file_ext = os.path.splitext(results[1])[1]
        if results:
            args_list = []
            for idx, img_url in enumerate(results, start=1):
                file_name = f"Page_{idx:03}{file_ext}"
                path_file = construct_npath([name, file_name])
                args_list.append((img_url, idx, path_file, headers))

            with concurrent.futures.ThreadPoolExecutor(max_workers = 5) as executor:
                executor.map(download_page, args_list)
        if pdf:
            images_to_pdf(folder_path)
    
    def delete(self,doujin):
        doujin_name = get_name(doujin)
        doujin_name =sanitize_filename(doujin_name)[:75]
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        doujin_folder = os.path.join(parent_dir, "Downloads", "Saved_Doujins",doujin_name)
        if os.path.exists(doujin_folder):
            shutil.rmtree(doujin_folder)
            print(f"Deleted doujin folder: {doujin_folder}")
        else:
            print(f"Folder does not exist{doujin_folder}")


