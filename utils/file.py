import os 
import shutil
from fastapi import UploadFile
from typing import List


class File(object):
    def __init__(self):
        self.BASE_TEMP_DIR = os.path.join(os.getcwd(), "uploads")
        os.makedirs(self.BASE_TEMP_DIR, exist_ok=True)
        self.BASE_DATA_DIR=os.path.join(os.getcwd(), "data")
        os.makedirs(self.BASE_DATA_DIR, exist_ok=True)
        


    def save_uploaded_files(self, files:List[UploadFile])->List[str]:
        saved_files = []

        for file in files:
            filename = file.filename
            file_path = os.path.join(self.BASE_TEMP_DIR, filename)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            saved_files.append(file_path)

        return saved_files

    def cleanup_temp_files(self):
        for filename in os.listdir(self.BASE_TEMP_DIR):
            file_path = os.path.join(self.BASE_TEMP_DIR, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)  
                    print(f"Deleted temp file: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")


    def write_markdown_file(self, file_name:str, content:str|list)->str:
        
        file_path=os.path.join(self.BASE_DATA_DIR, f"{file_name}_output.md")
        
        if isinstance(content, list):
            page_content = ""
        
            for _content in content:
                page_content += _content
        else:
            page_content = content
            
        with open(file_path, "w", encoding="utf-8") as file:
            print("Writing markdown file...")
            file.write(page_content)
            
        return file_path
            