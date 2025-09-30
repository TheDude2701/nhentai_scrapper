from setuptools import setup, find_packages

setup(
    name="nhentai",
    version="1.0",
    py_modules=["main"],
    packages=find_packages(), 
    entry_points={
        "console_scripts": [
            "nhentai = nhentai_scrapper.main:main",
        ],
    },
    install_requires=[
        "beautifulsoup4==4.13.3",
        "Pillow==9.3.0",
        "playwright==1.55.0",
        "requests==2.32.3",
        "lxml",
        "concurrent-futures; python_version<'3.2'"

    ],
)