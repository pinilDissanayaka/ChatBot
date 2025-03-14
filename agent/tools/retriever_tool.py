from langchain.tools.retriever import create_retriever_tool
from utils import VectorStore


def get_retriever_tool(web_name):
    """
    Return a retriever tool that is able to search and retrieve information from a given web_name's vector store.

    Args:
        web_name (str): The name of the website to get a retriever tool for.

    Returns:
        retriever_tool (RetrieverTool): A retriever tool that is able to search and retrieve information from the given web_name's vector store.
    """
    retriever_tool = create_retriever_tool(
        VectorStore().get_vector_store(web_name=web_name),
        f"retrieve_about_Website",
        f"Search and return information about retrieve_about {web_name} Website.",
    )

    
    return retriever_tool