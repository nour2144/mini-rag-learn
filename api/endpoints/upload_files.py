import aiofiles
import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from ..controllers import DataController, FileController

data_router = APIRouter(prefix="/data", tags=["data"])
@data_router.post("/upload")
async def upload_file(file_id: str, file: UploadFile = File(...,description="File to upload")):
    """Endpoint to upload a file. Validates the file type and size before processing."""

    if not DataController().validate_file(file):
            raise HTTPException(status_code=400, detail="Invalid file type.")
    file_controller = FileController()
    file_path = file_controller.get_file_path(file_id)
    file_path = os.path.join(file_path, file.filename)
    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read(file_controller.app_settings.file_chunk_size*1024)
            await out_file.write(content)
            return {"message": "File uploaded successfully", "filename": file.filename, "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
