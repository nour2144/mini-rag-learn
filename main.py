from fastapi import FastAPI
from dotenv import load_dotenv
from api import base
app = FastAPI() 

app.include_router(base.base_router)
# @ app.get("/")
# def read_root():
#     return {"Signal": "hi"}