#Libraries
import os
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .enums import ResponseEnum
from .helper.config import get_settings

# Base API Router
base_router = APIRouter(tags=["base"])
# Base API Endpoints
# Deprecated endpoint for backward compatibility
@base_router.get("/base_v1",deprecated=True)
async def read_root():
    app_name = os.getenv("APP_NAME")
    return JSONResponse(
        content={"App Name": app_name, "Signal": ResponseEnum.HTTP_BASE.value}, status_code=status.HTTP_200_OK
        )
# New endpoint with structured response model
class ResponseBody(BaseModel):
    app_name: str
    signal: str
@base_router.get("/base_v2", response_model=ResponseBody, deprecated=True)
async def read_root_v2():
    app_name = os.getenv("APP_NAME")
    return ResponseBody(app_name=app_name, signal=ResponseEnum.HTTP_BASE.value)

# New endpoint with Settings
@base_router.get("/", response_model=ResponseBody)
async def read_root_v3(settings= Depends(get_settings)):
    return ResponseBody(app_name=settings.app_name, signal=ResponseEnum.HTTP_BASE.value)