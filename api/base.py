from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from .enums.ResponseEnum import ResponseEnum
base_router = APIRouter(tags=["base"])
@base_router.get("/")
def read_root():
    return JSONResponse(
        content={"Signal": ResponseEnum.HTTP_BASE.value}, status_code=status.HTTP_200_OK
        )