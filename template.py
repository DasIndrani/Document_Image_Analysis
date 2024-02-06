import os 
from pathlib import Path 
import logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s]: %(message)s")


project_name = "Document_Image_Analysis"


list_of_files =[
    "setup.py",
    "requirements.txt",
    f"{project_name}/components/main.py",
    f"{project_name}/logger.py",
    f"{project_name}/exception.py",
    "app.py"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Create directory: {filedir} for the file {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")
    
    else:
        logging.info(f"{filename} is already exists")



