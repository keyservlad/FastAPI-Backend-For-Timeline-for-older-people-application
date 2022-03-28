import datetime
from fastapi import APIRouter, Query, Response
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