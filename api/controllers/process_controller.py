from .base_controller import BaseController
from .file_controller import FileController
import magic
import os
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ..enums import ResponseEnum
from fastapi import HTTPException
class ProcessController(BaseController):
    def __init__(self, folder_id: str, file_id: str):
        super().__init__()
        self.file_path = FileController().get_file_path(folder_id, file_id)

    def get_file_type(self, file_id):
        return os.path.splitext(file_id)[-1]
    
    def get_file_loader(self, file_type:str):
        if not os.path.exists(self.file_path):
            raise HTTPException(status_code=404, detail=ResponseEnum.FILE_NOT_FOUND.value)
        if file_type == '.pdf':
            return PyMuPDFLoader(self.file_path)
        elif file_type == '.txt':
            return TextLoader(self.file_path, encoding='utf-8')
        
        else:
            raise HTTPException(status_code=400, detail=ResponseEnum.LOADER_INITIALIZATION_FAILURE.value)
    
    def get_file_documents(self, file_id):
        file_type = self.get_file_type(file_id)
        loader = self.get_file_loader(file_type)
        try:
            documents = loader.load()
            return documents
        except Exception as e:
            raise HTTPException(status_code=400, detail='error loading file: ' + str(e))
        
    def get_file_chunks(self, file_id: str, documents: list, chunk_size: int = 100, chunk_overlap: int = 20):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap,length_function=len)
        file_texts = [doc.page_content for doc in documents]
        file_metadata = [doc.metadata for doc in documents]

        chunks = text_splitter.create_documents(file_texts, metadatas=file_metadata)
        return chunks