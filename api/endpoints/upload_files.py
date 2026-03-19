from fastapi import APIRouter, UploadFile, File, HTTPException
from ..controllers import DataController


data_router = APIRouter(prefix="/data", tags=["data"])
@data_router.post("/upload")
async def upload_file(file: UploadFile = File(...,description="File to upload")):
    """Endpoint to upload a file. Validates the file type and size before processing."""

    data_controller = DataController()
    if not data_controller.validate_file(file):
            raise HTTPException(status_code=400, detail="Invalid file type.")

    
    return {"filename": file.filename, "content_type": file.content_type, "signal": "File validation successful."}