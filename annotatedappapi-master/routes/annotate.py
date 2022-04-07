import datetime
from fastapi import APIRouter, Query, Response
from fastapi import FastAPI, File, UploadFile, Form
from services.annotate_query_services import AnnotateQueryService
from models.annotate import Annotate
from models.annoate_test import AnnotateTest

router = APIRouter()
service = AnnotateQueryService()

@router.get('/home/{home}/annotate')
def get_home_annoate(home:str):
    return service.get_home_annotate(home)

@router.post('/create')
async def insert_home_annoate(annotate:AnnotateTest):
    return service.insert_home_annotate(annotate)

@router.put('/home')
async def update_home_annotate(home:str, start:int, end:int, annotate:AnnotateTest):
    return service.update_home_annotate(home, start, end, annotate)


# pip install python-multipart

@router.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}

@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file}


@router.post('/file/')
async def get_user(
        file: bytes = File(...),
        fileb: UploadFile = File(...),
        notes: str = Form(...)
):

    contents = await fileb.read()

    with open( fileb.filename, "wb") as f:
        f.write(contents)


    return ( {
        'file_size': len(file),
        'file_name': fileb.filename,
        'notes': notes,
        'file_content_type': fileb.content_type
    })