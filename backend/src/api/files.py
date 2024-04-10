from fastapi import APIRouter
from fastapi import UploadFile, File
from fastapi.responses import HTMLResponse
from typing import Annotated
from ..services.files import process_file

router = APIRouter(
    prefix='/file',
    tags=['file']
)


@router.post("/upload")
async def upload_files(files: list[UploadFile]):
    _files = await process_file(file for file in files)
    return _files


