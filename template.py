import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')
logging.info("Hello everyone, welcome to the project.")

list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    ".gitignore",
    "src/prompt.py",
    ".env",
    "setup.py",
    "research/trials.ipynb",  # Corrected typo: 'trails' to 'trials'
    "app.py",
    "requirements.txt"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir = filepath.parent
    filename = filepath.name
    print(filename)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Created directory {filedir} for the file {filename}")

    if not filepath.exists():
        filepath.touch()
        logging.info(f"Created empty file {filename}")
    else:
        logging.info(f"File {filename} already exists")
