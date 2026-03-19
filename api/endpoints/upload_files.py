from fastapi import APIRouter, UploadFile, File, HTTPException
from ..controllers import DataController


data_router = APIRouter(prefix="/data", tags=["data"])
@data_router.post("/upload")
async def upload_file(files: list[UploadFile] = File(...,description="Multiple files to upload")):
    for file in files:
        data_controller = DataController()
        if not data_controller.validate_file(file):
            raise HTTPException(status_code=400, detail="Invalid file type.")
    
    return {"filename": files.filename, "content_type": files.content_type}