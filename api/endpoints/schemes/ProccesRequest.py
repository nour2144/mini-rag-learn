from pydantic import BaseModel, Field

class ProcessRequest(BaseModel):
    folder_id: str = Field(..., description="ID of the folder containing the file to process")
    file_id: str = Field(None, description="ID of the file to process")
    file_type: str = Field(None, description="Type of the file to process (e.g., '.txt', '.pdf')")
    chunk_size: int = Field(100, description="Size of each chunk in characters")
    chunk_overlap: int = Field(20, description="Number of overlapping characters between chunks")