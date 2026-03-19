from fastapi import FastAPI, status
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

load_dotenv()  # Load environment variables from .env file

from api import base_router
from api.endpoints import data_router
app = FastAPI()

app.include_router(base_router)
app.include_router(data_router)