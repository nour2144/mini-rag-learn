import aiofiles
import os
from fastapi import APIRouter, Path, UploadFile, File, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from ..controllers import DataController, FileController, ProcessController
from ..models import FolderModel
from ..enums import ResponseEnum

data_router = APIRouter(prefix="/data", tags=["data"])
@data_router.post("/upload")
async def upload_file(request: Request, folder_id: str, file: UploadFile = File(...,description="File to upload")):
    """Endpoint to upload a file. Validates the file type and size before processing."""
    folder_model = FolderModel(db= request.app.db)
    folder = await folder_model.get_folder_or_creare_one(folder_id)

    DataController().validate_file(file)

    file_controller = FileController()
    file_path = file_controller.get_file_path(folder_id, file.filename)
    if os.path.exists(file_path):
        raise HTTPException(status_code=400, detail=f"File with name '{file.filename}' already exists.")
    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read(file_controller.app_settings.file_chunk_size*1024)
            await out_file.write(content)
            return {"message": ResponseEnum.FILE_UPLOAD_SUCCESS.value, "filename": file.filename, "file_path": file_path, 'folder_id': str(folder._id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=ResponseEnum.FILE_UPLOAD_FAILURE.value)
    
@data_router.post("/process")
async def process_file(folder_id: str, file_id: str, chunk_size: int = 100, chunk_overlap: int = 20):
    """Endpoint to process an uploaded file."""

    process_controller = ProcessController(folder_id, file_id)
    documents = process_controller.get_file_documents(file_id)
    chunks = process_controller.get_file_chunks(file_id, documents, chunk_size, chunk_overlap)
    if not chunks or len(chunks) == 0:
        raise HTTPException(status_code=400, detail=ResponseEnum.FILE_PROCESSING_FAILURE.value)
    
    return {"message": ResponseEnum.FILE_PROCESSING_SUCCESS.value, "chunk_count": len(chunks), "chunks": chunks}