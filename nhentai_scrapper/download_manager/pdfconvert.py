import os
from PIL import Image
import platform
import subprocess



def images_to_pdf(folder_path):
    folder_name = os.path.basename(os.path.normpath(folder_path))
    output_pdf = os.path.join(folder_path, f"{folder_name}.pdf")

    images = []
    image_files=[]
    for file in sorted(os.listdir(folder_path)):
        if file.lower().endswith((".jpg", ".png",".jpeg",".webp")):
            img_path = os.path.join(folder_path, file)
            img = Image.open(img_path).convert("RGB")
            images.append(img)
            image_files.append(img_path)

    if images:
        images[0].save(output_pdf, save_all=True, append_images=images[1:])
        for file in image_files:
                os.remove(file)
        print(f"PDF saved as: {output_pdf}")
    else:
        print("No images found in folder.")

def open_pdf(folder_path):
    folder_name = os.path.basename(os.path.normpath(folder_path))
    pdf_path = os.path.abspath(os.path.join(folder_path, f"{folder_name}.pdf"))    
    print(pdf_path)
    system = platform.system()
    try:
        if system == "Windows":
            os.startfile(pdf_path)
        elif system == "Darwin":  # macOS
            subprocess.run(["open", pdf_path])
        else:  # Linux 
            subprocess.run(["xdg-open", pdf_path])
    except Exception as e:
        print(f"Could not open PDF: {e}")
