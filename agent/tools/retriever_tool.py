from langchain.tools.retriever import create_retriever_tool
from utils import get_vector_store


def get_retriever_tool(vector_store_path, web_name):
    retriever_tool = create_retriever_tool(
        get_vector_store(store_path=vector_store_path, web_name=web_name),
        f"retrieve_about_Website",
        f"Search and return information about retrieve_about {web_name} Website.",
    )

    
    return retriever_tool