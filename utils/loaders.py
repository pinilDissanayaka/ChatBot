import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    JSONLoader,
    UnstructuredMarkdownLoader,
    UnstructuredPowerPointLoader,
    Docx2txtLoader

)
from typing import List


class Loader(object):
    def __init__(self, file_paths: List[str] = None, base_url: str = None, clean_text: str = None):
        self.file_paths = file_paths
        self.base_url = base_url
        self.clean_text = clean_text

    async def __pdf_loader(self, file_path: str) -> list:
        loop = asyncio.get_event_loop()
        loader = PyPDFLoader(file_path)
        return await loop.run_in_executor(None, loader.load)

    async def __pptx_loader(self, file_path: str) -> list:
        loop = asyncio.get_event_loop()
        loader = UnstructuredPowerPointLoader(file_path)
        return await loop.run_in_executor(None, loader.load)

    async def __text_loader(self, file_path: str) -> list:
        loop = asyncio.get_event_loop()
        loader = TextLoader(file_path)
        return await loop.run_in_executor(None, loader.load)

    async def __csv_loader(self, file_path: str) -> list:
        loop=asyncio.get_event_loop()
        loader = CSVLoader(file_path)
        return await self.loop.run_in_executor(None, loader.load)
    
    async def __json_loader(self, file_path: str) -> list:
        loop = asyncio.get_event_loop()
        loader = JSONLoader(file_path)
        return await loop.run_in_executor(None, loader.load)

    async def __markdown_loader(self, file_path: str) -> list:
        loop = asyncio.get_event_loop()
        loader = UnstructuredMarkdownLoader(file_path)
        return await loop.run_in_executor(None, loader.load)
    
    async def __docx_loader(self, file_path: str) -> list:
        loop = asyncio.get_event_loop()
        loader = Docx2txtLoader(file_path)
        return await loop.run_in_executor(None, loader.load)

    async def __load_file(self) -> List[list]:
        tasks = []
        for file_path in self.file_paths:
            file_path_lower = file_path.lower()
            if file_path_lower.endswith(".pdf"):
                tasks.append(self.__pdf_loader(file_path))
            elif file_path_lower.endswith(".pptx"):
                tasks.append(self.__pptx_loader(file_path))
            elif file_path_lower.endswith(".txt"):
                tasks.append(self.__text_loader(file_path))
            elif file_path_lower.endswith(".csv"):
                tasks.append(self.__csv_loader(file_path))
            elif file_path_lower.endswith(".json"):
                tasks.append(self.__json_loader(file_path))
            elif file_path_lower.endswith(".md"):
                tasks.append(self.__markdown_loader(file_path))
            elif file_path_lower.endswith(".docx"):
                tasks.append(self.__docx_loader(file_path))
            else:
                raise ValueError(f"Unsupported file type: {file_path}")

        return await asyncio.gather(*tasks)

    async def __scrape_page(self, url: str) -> list:
        visited_urls = set()
        scraped_content = []

        async def __recursive_scrape(session, url):
            if url in visited_urls:
                return
            print(f"Scraping: {url}")
            visited_urls.add(url)

            try:
                async with session.get(url) as response:
                    if response.status != 200:
                        print(f"Failed to retrieve {url}")
                        return
                    text = await response.text()
                    soup = BeautifulSoup(text, 'html.parser')
                    page_content = soup.get_text(separator='\n', strip=True)
                    scraped_content.append(page_content)

                    for link in soup.find_all('a', href=True):
                        next_url = urljoin(url, link['href'])
                        if next_url.startswith(url):
                            await __recursive_scrape(session, next_url)

            except Exception as e:
                print(f"Error scraping {url}: {e}")

        async with aiohttp.ClientSession() as session:
            await __recursive_scrape(session, url)

        return scraped_content

    async def web_loader(self) -> str:
        if self.base_url:
            web_contents = await self.__scrape_page(self.base_url)
            return ''.join(web_contents)
        return ""

    async def load(self) -> str:
        text_content = ""

        if self.file_paths:
            loaded_documents = await self.__load_file()
            for doc_group in loaded_documents:
                for doc in doc_group:
                    text_content += doc.page_content

        if self.base_url:
            text_content += await self.web_loader()

        if self.clean_text:
            text_content += self.clean_text

        return text_content.replace("\n", "")
        
        

                
        
    