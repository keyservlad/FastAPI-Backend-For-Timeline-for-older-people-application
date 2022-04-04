from turtle import home
from fastapi import APIRouter,Depends
from services.annotate_query_services import AnnotateQueryService
from models.annotate import Annotate
from models.annoate_test import AnnotateTest
from models.annotations import Annotations
from schemas.annotations import AnnotationsCreate
from sqlalchemy.orm import Session
from typing import Any
from api import  deps
from crud import crudAnnotation
# import the error handling libraries for psycopg2
from psycopg2 import OperationalError

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

@router.post("/createAnnotations", response_model=AnnotationsCreate)
def create_annotation(
    *,
    db: Session = Depends(deps.get_db),
    annotation_in:AnnotationsCreate
) -> Any:
    """
    Create new Annotation.
    """
    print(annotation_in)
    try:
            annotation = crudAnnotation.annotations.create(db, obj_in=annotation_in)
            return annotation
    except OperationalError as error:
        print ("Oops! An exception has occured:", error)
        print ("Exception TYPE:", type(error))
        return {
            "code":"505",
            "message":"Oops! An exception has occured:"
        }