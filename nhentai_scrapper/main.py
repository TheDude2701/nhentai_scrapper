import argparse
import sys
import os
from nhentai_scrapper.download_manager.downloader import *
from nhentai_scrapper.download_manager.pdfconvert import open_pdf
from nhentai_scrapper.download_manager.nHentaiScraper import get_name, get_code
from nhentai_scrapper.download_manager.download_path import sanitize_filename


def main():
    parser = argparse.ArgumentParser(prog="nhentai", description="Doujin download tool")
    subparsers = parser.add_subparsers(dest="command")

    dl_parser = subparsers.add_parser("download", help="Download by sauce ID")
    dl_parser.add_argument("sauce", help="The NHentai sauce code")
    dl_parser.add_argument(
        "--pdf",
        action="store_true", 
        help="Convert downloaded images into a PDF and delete the originals"
    )

    delete_parser = subparsers.add_parser("delete", help = "Delete a downloaded doujin by sauce code")
    delete_parser.add_argument("sauce", help = "The NHentai sauce code")

    open_parser = subparsers.add_parser("open", help="Open the downloaded pdf")
    open_parser.add_argument("sauce", help="NHentai Sauce Code")

    lookup_parser = subparsers.add_parser("lookup", help="return sauce code based on title")
    lookup_parser.add_argument(
        "--title",
        type=str, 
        help="Search the title of the doujin by the title, Returns code"
    )
    lookup_parser.add_argument(
        "--code",
        type=str, 
        help="Search the title of the doujin by the code, Returns title"
    )

    downloaded_parser = subparsers.add_parser("doujins", help = "List of downloaded doujins")

    args = parser.parse_args()
    if args.command == "download":
        print(f"Downloading doujin {args.sauce}...")
        download = downloadManager()
        print("Probing for valid img links (This will take longer if number of pages are large)")
        downloaded = download.download_doujin(args.sauce, pdf=args.pdf)
        if downloaded == 1:
            return
    
    if args.command == "delete":
        print(f"Deleting Doujin: {args.sauce}")
        download = downloadManager()
        download.delete(args.sauce)
        print("Successfully Deleted")
    
    if args.command == "open":
        print(f"Opening Doujin: {args.sauce}")
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        script1_dir = os.path.dirname(parent_dir)
        doujin_folders = os.path.join(script1_dir, "Downloads", "Saved_Doujins")
        if os.path.exists(doujin_folders):
            found = False
            for name in os.listdir(doujin_folders):
                match = re.match(r"^(\d{1,6})-", name)
                if match and match.group(1) == args.sauce:
                    doujin_path = os.path.join(doujin_folders, name)
                    if os.path.isdir(doujin_path):
                        for file in os.listdir(doujin_path):
                            if file.endswith(".pdf"):
                                pdf_path = os.path.join(doujin_path, file)
                                print(f"Opening {pdf_path}")
                                os.startfile(pdf_path)  # Windows only
                                found = True
                                break
                    if found:
                        break
            if not found:
                print("No Doujin found matching that code")
        else:
            print("You don't have that doujin downloaded!")
    
    if args.command == "lookup":
        if args.code:
            name = get_name(args.code)
            print(name)   
        elif args.title:
            code = get_code(args.title)
            print(code) 
        else:
            print("Please provide either --code or --title")
    
    if args.command  == "doujins":
        child_dir = os.path.dirname(os.path.abspath(__file__))
        script_dir = os.path.dirname(child_dir)
        doujin_folder = os.path.join(script_dir, "Downloads", "Saved_Doujins")
        if os.path.exists(doujin_folder):
            saved_doujins = [
                name for name in os.listdir(doujin_folder)
                if os.path.isdir(os.path.join(doujin_folder, name))
            ]
            if saved_doujins:
                print("Saved Doujins:")
                for doujin in saved_doujins:
                    print(f"- {doujin}")
            else:
                print("No doujins saved yet.")
        else:
            print("No Saved_Doujins folder found.")



if __name__ == "__main__":
    main()