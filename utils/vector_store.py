import os
from turtle import st
from .config import embeddings, llm
from langchain_experimental.text_splitter import SemanticChunker
from langchain_chroma import Chroma
        
def get_vector_store(store_path: str, web_name: str):
    vector_store = Chroma(
        collection_name=f"{web_name}",
        embedding_function=embeddings,
        persist_directory=store_path,  
    )
    
    return vector_store.as_retriever()
    
    

        


