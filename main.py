from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from api.helper.config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient
load_dotenv()  # Load environment variables from .env file  /Deprecated 

from api import base_router
from api import data_router
settings = get_settings()
@asynccontextmanager
async def lifespan(app):
    app.db_client = AsyncIOMotorClient(settings.mongo_url)
    app.db = app.db_client[settings.mongo_db_name]
    print("✅ DB connected")

    yield   # ← app runs here

    app.db_client.close()
    print("❌ DB disconnected")
app = FastAPI(title=settings.app_name, version=settings.app_version,lifespan=lifespan)
# @app.on_event("startup")
# async def startup_db_client():
#     app.db_client = AsyncIOMotorClient(settings.mongo_url)
#     app.db = app.db_client[settings.mongo_db_name]
#     return JSONResponse(content={"message": "Database connection established"}, status_code=status.HTTP_200_OK)
# @app.on_event("shutdown")
# async def shutdown_db_client():
#     app.db_client.close()
#     return JSONResponse(content={"message": "Database connection closed"}, status_code=status.HTTP_200_OK)

app.include_router(base_router)
app.include_router(data_router)