import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from langchain_community.document_loaders import PyPDFLoader, TextLoader, JSONLoader, UnstructuredMarkdownLoader, UnstructuredPowerPointLoader
from langchain_community.document_loaders import UnstructuredPowerPointLoader
from typing import List


class Loader(object):
    def __init__(self, file_paths: List[str]=None, base_url: str = None, clean_text:str=None):
        self.file_paths = file_paths
        self.base_url = base_url
        self.clean_text = clean_text

    def __pdf_loader(self, file_path: str) -> list:
        loader = PyPDFLoader(file_path)
        return loader.load()

    def __pptx_loader(self, file_path: str) -> list:
        loader = UnstructuredPowerPointLoader(file_path)
        return loader.load()

    def __text_loader(self, file_path: str) -> list:
        loader = TextLoader(file_path)
        return loader.load()

    def __csv_loader(self, file_path: str) -> list:
        loader = TextLoader(file_path)
        return loader.load()

    def __json_loader(self, file_path: str) -> list:
        loader = JSONLoader(file_path)
        return loader.load()

    def __markdown_loader(self, file_path: str) -> list:
        loader = UnstructuredMarkdownLoader(file_path)
        return loader.load()

    def __load_file(self) -> List[list]:
        loaded_documents = []
        for file_path in self.file_paths:
            file_path_lower = file_path.lower()

            if file_path_lower.endswith(".pdf"):
                content = self.__pdf_loader(file_path)
            elif file_path_lower.endswith(".pptx"):
                content = self.__pptx_loader(file_path)
            elif file_path_lower.endswith(".txt"):
                content = self.__text_loader(file_path)
            elif file_path_lower.endswith(".csv"):
                content = self.__csv_loader(file_path)
            elif file_path_lower.endswith(".json"):
                content = self.__json_loader(file_path)
            elif file_path_lower.endswith(".md"):
                content = self.__markdown_loader(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_path}")

            loaded_documents.append(content)

        return loaded_documents

    def __scrape_page(self, url: str) -> list:
        visited_urls = set()
        scraped_content = []

        def __recursive_scrape(url):
            if url in visited_urls:
                return
            print(f"Scraping: {url}")
            visited_urls.add(url)

            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to retrieve {url}")
                return

            soup = BeautifulSoup(response.text, 'html.parser')
            page_content = soup.get_text(separator='\n', strip=True)
            scraped_content.append(page_content)

            for link in soup.find_all('a', href=True):
                next_url = urljoin(url, link['href'])
                if next_url.startswith(url): 
                    __recursive_scrape(next_url)

        __recursive_scrape(url)
        return scraped_content

    def web_loader(self) -> str:
        text_content = ""
        if self.base_url:
            web_contents = self.__scrape_page(self.base_url)

            if isinstance(web_contents, list):
                for web_content in web_contents:
                    text_content += web_content
            else:
                text_content = web_contents

        return text_content

    def load(self) -> str:
        text_content = ""
        if self.file_paths is not None:
            loaded_documents = self.__load_file()

            if isinstance(loaded_documents, list):
                for _loaded_documents in loaded_documents:
                    if isinstance(_loaded_documents, list):
                        for document_content in _loaded_documents:
                            text_content += document_content.page_content
                    else:
                        text_content += _loaded_documents.page_content
            else:
                text_content = loaded_documents.page_content

        if self.base_url is not None:
            text_content += self.web_loader()
        if self.clean_text is not None:
            text_content += self.clean_text
            
        text_content = text_content.replace("\n", "")

        return text_content

        
        

                
        
    