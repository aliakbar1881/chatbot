from typing import List, Optional
from langchain_core.documents import Document
from langchain_community.document_loaders.base import BaseLoader

class CustomDocumentLoader(BaseLoader):
    """
    A custom document loader that demonstrates how to create a loader for specific file types or data sources.
    This example shows how to load documents from a custom source with metadata.
    """

    def __init__(self, file_path: str, encoding: str = "utf-8", metadata: Optional[dict] = None):
        """
        Initialize the custom document loader.

        Args:
            file_path (str): Path to the file or data source
            encoding (str, optional): File encoding. Defaults to "utf-8".
            metadata (dict, optional): Additional metadata to add to all documents.
        """
        self.file_path = file_path
        self.encoding = encoding
        self.metadata = metadata or {}

    def load(self) -> List[Document]:
        """
        Load documents from the source.

        Returns:
            List[Document]: A list of Document objects.
        """
        documents = []
        
        try:
            # Example: Reading a custom file format
            with open(self.file_path, 'r', encoding=self.encoding) as file:
                # This is a simple example. Modify this part based on your file format
                for line_number, line in enumerate(file, 1):
                    if line.strip():  # Skip empty lines
                        # Create metadata for this specific document
                        metadata = {
                            "source": self.file_path,
                            "line_number": line_number,
                            **self.metadata  # Include any additional metadata
                        }
                        
                        # Create a Document object
                        doc = Document(
                            page_content=line.strip(),
                            metadata=metadata
                        )
                        documents.append(doc)
                        
        except Exception as e:
            raise ValueError(f"Error loading document from {self.file_path}: {str(e)}")
        
        return documents

    def lazy_load(self) -> List[Document]:
        """
        Lazily load documents from the source.
        Useful for large files that shouldn't be loaded into memory at once.

        Yields:
            Document: A Document object.
        """
        try:
            with open(self.file_path, 'r', encoding=self.encoding) as file:
                for line_number, line in enumerate(file, 1):
                    if line.strip():
                        metadata = {
                            "source": self.file_path,
                            "line_number": line_number,
                            **self.metadata
                        }
                        
                        yield Document(
                            page_content=line.strip(),
                            metadata=metadata
                        )
                        
        except Exception as e:
            raise ValueError(f"Error lazy loading document from {self.file_path}: {str(e)}")


# Example usage:
if __name__ == "__main__":
    # Example 1: Basic usage
    loader = CustomDocumentLoader(
        file_path="example.txt",
        metadata={"category": "example", "language": "en"}
    )
    
    # Load all documents at once
    documents = loader.load()
    
    # Example 2: Lazy loading for large files
    loader = CustomDocumentLoader("large_file.txt")
    for doc in loader.lazy_load():
        print(f"Processing document: {doc.page_content[:50]}...")  # Process each document one at a time 