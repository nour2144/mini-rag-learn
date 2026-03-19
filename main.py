from fastapi import FastAPI, status
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

load_dotenv()  # Load environment variables from .env file

from api import base
app = FastAPI() 

app.include_router(base.base_router)