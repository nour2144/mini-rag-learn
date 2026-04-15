import aiofiles
import os
from fastapi import APIRouter, Path, UploadFile, File, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from api.endpoints.schemes.ProccesRequest import ProcessRequest
from ..controllers import DataController, FileController, ProcessController
from ..models import FolderModel, ChunkModel, AssetModel
from ..enums import ResponseEnum
from ..models.db_schemes import ChunksDB, AssetDB

data_router = APIRouter(prefix="/data", tags=["data"])
@data_router.post("/upload")
async def upload_file(request: Request, folder_id: str, file: UploadFile = File(...,description="File to upload")):
    """Endpoint to upload a file. Validates the file type and size before processing."""
    folder_model = await FolderModel.create_instance(db= request.app.db)
    folder,folder_DB_id = await folder_model.get_folder_or_creare_one(folder_id)

    await DataController().validate_file(file)

    file_controller = FileController()
    file_path = file_controller.get_file_path(folder_id, file.filename)
    if os.path.exists(file_path):
        raise HTTPException(status_code=400, detail=f"File with name '{file.filename}' already exists.")
    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read(file_controller.app_settings.file_chunk_size*1024)
            await out_file.write(content)
            asset_model = await AssetModel.create_instance(db= request.app.db)
            asset_resource = AssetDB(
                asset_folder_id=folder_DB_id,
                asset_name=file.filename,
                asset_type=file.content_type
            )
            asset, asset_id = await asset_model.create_asset(asset_resource)

            return {"message": ResponseEnum.FILE_UPLOAD_SUCCESS.value, "folder_id": folder_DB_id, "file_path": file_path, 'folder_id': str(folder_DB_id), 'asset_id': asset_id}
    except Exception as e:
        print(f"Error uploading file: {e}")
        raise HTTPException(status_code=400, detail=ResponseEnum.FILE_UPLOAD_FAILURE.value)
    
@data_router.post("/process")
async def process_file(request: Request, process_request: ProcessRequest):
    """Endpoint to process an uploaded file."""
    folder_id = process_request.folder_id
    file_type = process_request.file_type
    chunk_size = process_request.chunk_size
    chunk_overlap = process_request.chunk_overlap

    folder_model = await FolderModel.create_instance(db= request.app.db)
    _, folder_DB_id = await folder_model.get_folder_or_creare_one(folder_id)

    file_ids = []
    asset_model = await AssetModel.create_instance(db= request.app.db)
    if process_request.file_id:
        file = await asset_model.get_asset(asset_folder_id=folder_DB_id, asset_name=process_request.file_id)
        if not file:
            raise HTTPException(status_code=404, detail=ResponseEnum.FILE_ID_NOT_FOUND.value)
        file_ids.append(file.asset_name)
    else:
        files = await asset_model.get_all_assets(asset_folder_id=folder_DB_id, asset_type=file_type)
        file_ids = [file.asset_name for file in files]
        
        
    num_record = 0
    num_files = 0
    num_files = len(file_ids)
    if num_files == 0:
            raise HTTPException(status_code=400, detail=ResponseEnum.NO_FILES_TO_PROCESS.value)
    for file_id in file_ids:
        process_controller = ProcessController(folder_id, file_id)
        documents = process_controller.get_file_documents(file_id)

        if not documents or len(documents) == 0:
            continue

        chunks = process_controller.get_file_chunks(file_id, documents, chunk_size, chunk_overlap)
        if not chunks or len(chunks) == 0:
            raise HTTPException(status_code=400, detail=ResponseEnum.FILE_PROCESSING_FAILURE.value)
        
        # return {"message": ResponseEnum.FILE_PROCESSING_SUCCESS.value, "chunk_count": len(chunks), "chunks": chunks}
        file_chunks = [
            ChunksDB(
                chunk_text=chunk.page_content,
                chunk_metadata=chunk.metadata,
                chunk_order=i+1,
                chunk_folder_id=folder_DB_id
            ) for i,chunk in enumerate(chunks)
        ]
        chunk_model = await ChunkModel.create_instance(db= request.app.db)
        num_record += await chunk_model.insert_many_chunks(file_chunks)
    return {"message": ResponseEnum.FILE_PROCESSING_SUCCESS.value, "chunk_count": num_record, "processed_files": num_files}