import os
from .config import embeddings, llm
from langchain_experimental.text_splitter import SemanticChunker
from langchain_chroma import Chroma


class VectorStore:
    def __init__(self) -> None:
        self.BASE_VECTOR_STORE_DIR = os.path.join(os.getcwd(), "vector")
        os.makedirs(self.BASE_VECTOR_STORE_DIR, exist_ok=True)

    def create_vector_store(self, web_name: str, content: list|str):
        store_path=os.path.join(self.BASE_VECTOR_STORE_DIR, web_name)
        
        if isinstance(content, str):
            content = [content]
        
        
        chunker=SemanticChunker(embeddings=embeddings)
        
        docs=chunker.create_documents(content)
        
        vector_store = Chroma(
            collection_name=f"{web_name}",
            embedding_function=embeddings,
            persist_directory=store_path, 
        )
        
        vector_store.add_documents(docs)
        
        return web_name
            
    def get_vector_store(self, web_name: str):
        
        store_path=os.path.join(self.BASE_VECTOR_STORE_DIR, web_name)
        
        vector_store = Chroma(
            collection_name=f"{web_name}",
            embedding_function=embeddings,
            persist_directory=store_path,  
        )
        
        return vector_store.as_retriever()
    
    

        


