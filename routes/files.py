import os
from fastapi import APIRouter, UploadFile, File
import markdown
from utils import Loader, File, VectorStore 
from typing import List, Optional
from database import session, Bot


file_upload_router = APIRouter(
    prefix="/files",
    tags=['Create vector store'],
)

@file_upload_router.post("/upload-files/")
async def upload_files(
    name: str,
    files: Optional[List[UploadFile]]=None,
    text: Optional[str] = None,
    web_url: Optional[str] = None,
):
    file_object=File()
    file_paths=file_object.save_uploaded_files(files=files)
    loader = Loader(file_paths=file_paths, base_url=web_url, clean_text=text) 
    content = loader.load()
    file_object.cleanup_temp_files()
    
    markdown_file_path=file_object.write_markdown_file(file_name=name, content=content)
        
    web_name=VectorStore().create_vector_store(web_name=name, content=content)
    
    new_bot=Bot(web_name=web_name, base_url=web_url)
    
    session.add(new_bot)
    session.commit()
    session.close()
    
    return {
        "message": "Vector store created successfully",
        "saved_files": content,
        "web_name": web_name
    }