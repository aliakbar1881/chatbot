from typing import List, Optional
import json
from datetime import datetime
from langchain_core.documents import Document
from langchain_community.document_loaders.base import BaseLoader

class ChatHistoryLoader(BaseLoader):
    """
    A specialized document loader for chat history files.
    Handles JSON files containing chat messages with timestamps and user information.
    """

    def __init__(self, file_path: str, metadata: Optional[dict] = None):
        """
        Initialize the chat history loader.

        Args:
            file_path (str): Path to the JSON chat history file
            metadata (dict, optional): Additional metadata to add to all documents
        """
        self.file_path = file_path
        self.metadata = metadata or {}

    def _parse_message(self, message: dict, message_index: int) -> Document:
        """
        Parse a single message into a Document object.

        Args:
            message (dict): The message dictionary
            message_index (int): Index of the message in the conversation

        Returns:
            Document: A Document object containing the message
        """
        # Extract message details
        content = message.get('content', '')
        timestamp = message.get('timestamp', '')
        user_id = message.get('user_id', 'unknown')
        message_type = message.get('type', 'text')

        # Create metadata for this message
        message_metadata = {
            "source": self.file_path,
            "message_index": message_index,
            "timestamp": timestamp,
            "user_id": user_id,
            "message_type": message_type,
            **self.metadata
        }

        # Create the document
        return Document(
            page_content=content,
            metadata=message_metadata
        )

    def load(self) -> List[Document]:
        """
        Load and parse the entire chat history file.

        Returns:
            List[Document]: A list of Document objects, each representing a chat message
        """
        documents = []

        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                chat_history = json.load(file)

                # Handle both single conversation and multiple conversation formats
                if isinstance(chat_history, list):
                    messages = chat_history
                elif isinstance(chat_history, dict):
                    messages = chat_history.get('messages', [])
                else:
                    raise ValueError("Invalid chat history format")

                # Process each message
                for idx, message in enumerate(messages):
                    doc = self._parse_message(message, idx)
                    documents.append(doc)

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in {self.file_path}: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error loading chat history from {self.file_path}: {str(e)}")

        return documents

    def lazy_load(self) -> List[Document]:
        """
        Lazily load chat messages from the file.
        Useful for large chat histories.

        Yields:
            Document: A Document object representing a chat message
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                chat_history = json.load(file)

                # Handle both single conversation and multiple conversation formats
                if isinstance(chat_history, list):
                    messages = chat_history
                elif isinstance(chat_history, dict):
                    messages = chat_history.get('messages', [])
                else:
                    raise ValueError("Invalid chat history format")

                # Yield each message as a document
                for idx, message in enumerate(messages):
                    yield self._parse_message(message, idx)

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in {self.file_path}: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error lazy loading chat history from {self.file_path}: {str(e)}")


# Example usage:
if __name__ == "__main__":
    # Example chat history file format:
    example_chat = {
        "conversation_id": "123",
        "messages": [
            {
                "content": "Hello, how can I help you today?",
                "timestamp": "2024-03-10T12:00:00Z",
                "user_id": "bot_1",
                "type": "text"
            },
            {
                "content": "I need help with my account",
                "timestamp": "2024-03-10T12:01:00Z",
                "user_id": "user_123",
                "type": "text"
            }
        ]
    }

    # Save example chat to a file
    with open("example_chat.json", "w") as f:
        json.dump(example_chat, f, indent=2)

    # Load the chat history
    loader = ChatHistoryLoader(
        file_path="example_chat.json",
        metadata={"source_type": "customer_service_chat"}
    )

    # Method 1: Load all messages at once
    documents = loader.load()
    for doc in documents:
        print(f"Message: {doc.page_content}")
        print(f"Metadata: {doc.metadata}\n")

    # Method 2: Load messages lazily
    for doc in loader.lazy_load():
        print(f"Processing message: {doc.page_content}") 