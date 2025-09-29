import argparse
from download_manager.downloader import *
from download_manager.pdfconvert import images_to_pdf, open_pdf
from download_manager.nHentaiScraper import get_name, get_code

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
    lookup_parser.add_argument("title", help="Title of the doujin")


    args = parser.parse_args()
    if args.command == "download":
        print(f"Downloading doujin {args.sauce}...")
        download = downloadManager()
        if download.download_doujin(args.sauce) == 1:
            return
        if args.pdf:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            doujin_name = get_name(args.sauce)
            target_folder = os.path.join(script_dir, "Downloads", "Saved_Doujins", doujin_name)
            images_to_pdf(target_folder)
    
    if args.command == "delete":
        print(f"Deleting Doujin: {args.sauce}")
        download = downloadManager()
        download.delete(args.sauce)
        print("Successfully Deleted")
    
    if args.command == "open":
        print(f"Opening Doujin: {args.sauce}")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        doujin_name = get_name(args.sauce)
        target_folder = os.path.join(script_dir, "Downloads", "Saved_Doujins", doujin_name)
        if not os.path.exists(target_folder):
            print("You don't have that doujin downloaded!")
        else:
            open_pdf(target_folder)
    if args.command == "lookup":
        get_code(args.title)



if __name__ == "__main__":
    main()