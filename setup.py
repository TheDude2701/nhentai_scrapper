from setuptools import setup, find_packages

setup(
    name="nHentai",
    version="0.1",
    py_modules=["main"],
    entry_points={
        "console_scripts": [
            "nHentai = main:main",
        ],
    },
    install_requires=[
        "beautifulsoup4==4.13.3",
        "Pillow==9.3.0",
        "playwright==1.55.0",
        "requests==2.32.3"
    ],
)