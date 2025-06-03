from logger import loguru
from langchain.vectorstores import faiss
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import WebBaseLoader
from langchain.document_loaders import xml
from langchain.document_loaders import CSVLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import JSONLoader
from langchain.document_loaders import powerpoint
from langchain.embeddings import HuggingFaceBgeEmbeddings


from app.utils.ocr_loader import OCR

class Index:
    def __init__(self, database: str):
        self.database = database
        self.embeddings = HuggingFaceBgeEmbeddings(model="BAAI/bge-m3")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.vectorstore = faiss.FAISS(self.embeddings, self.text_splitter)
    
    def load_data(self, filename: str):
        if filename.endswith(".txt"):
            loader = TextLoader(filename)
        elif filename.endswith(".pdf"):
            try:
                loader = PyPDFLoader(filename)
            except Exception as e:
                try:
                    pdf = OCR(filename)
                    loader = PyPDFLoader(filename)
                except Exception as e:
                    loguru.error(f"Error loading pdf file: {e}")

        elif filename.endswith(".xml"):
            loader = xml(filename)
        elif filename.endswith(".csv"):
            loader = CSVLoader(filename)
        elif filename.endswith(".docx"):
            loader = Docx2txtLoader(filename)
        elif filename.endswith(".json"):
            loader = JSONLoader(filename)
        elif filename.endswith(".pptx"):
            loader = powerpoint(filename)
        elif filename.endswith(".web"):
            loader = WebBaseLoader(filename)
        else:
            return {"message": "File not supported"}
        return loader.load()

    async def indexing(self, files: list[str]):
        try:
            for file in files:
                loaded_doc = self.load_data(file)
                if loaded_doc:
                    await self.vectorstore.aadd_documents(loaded_doc)
            return {"message": "Documents indexed successfully"}
        except Exception as e:
            loguru.error(f"Error during indexing: {e}")
            raise
        
    async def search(self, query: str):
        try:
            return await self.vectorstore.asimilarity_search(query, k=10)
        except Exception as e:
            loguru.error(f"Error during search: {e}")
            raise

    async def delete(self, document):
        try:
            return await self.vectorstore.adelete(document)
        except Exception as e:
            loguru.error(f"Error during deletion: {e}")
            raise

    async def update(self, document):
        try:
            return await self.vectorstore.aupdate(document)
        except Exception as e:
            loguru.error(f"Error during update: {e}")
            raise
    
    async def get_by_ids(self, ids: list[str]):
        try:
            return await self.vectorstore.aget_by_ids(ids)
        except Exception as e:
            loguru.error(f"Error retrieving documents by IDs: {e}")
            raise
    
    async def get_all(self):
        try:
            return await self.vectorstore.aget_all()
        except Exception as e:
            loguru.error(f"Error retrieving all documents: {e}")
            raise

    async def save(self, path: str):
        try:
            await self.vectorstore.save_local(path)
            return {"message": f"Vector store saved successfully to {path}"}
        except Exception as e:
            loguru.error(f"Error saving vector store: {e}")
            raise

    async def __call__(self):
        # read files from database
        files = []

        await self.indexing(files)
        self.save(self.vectorstore)