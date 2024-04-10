from fastapi import FastAPI
from src.api import files

app = FastAPI()

app.include_router(files.router)

