from turtle import home
from fastapi import APIRouter,Depends
from services.annotate_query_services import AnnotateQueryService
from models.annotate import Annotate
from models.annoate_test import AnnotateTest
from models.annotations import Annotations
from schemas.annotations import AnnotationsCreate,AnnotationsUpdate
from sqlalchemy.orm import Session
from typing import Any
from api import  deps
from crud import crudAnnotation
# import the error handling libraries for psycopg2
from psycopg2 import OperationalError

from fastapi import  HTTPException

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
            if not annotation:
               raise HTTPException(
                        status_code=400,
                        detail="The annotation with this activity already exists in the system.",
                        )
            return annotation
    except OperationalError as error:
        print ("Oops! An exception has occured:", error)
        print ("Exception TYPE:", type(error))
        return {
            "code":"505",
            "message":"Oops! An exception has occured:"
        }
@router.delete("/{id}", response_model=AnnotationsCreate)
def delete_annotation(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete an annotation.
    """
    annotation = crudAnnotation.annotations.get(db=db, id=id)
    if not annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")
    annotation = crudAnnotation.annotations.remove(db=db, id=id)
    return annotation

    
@router.put("/{id}", response_model=AnnotationsUpdate)
def update_annotation(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    annotation_in: AnnotationsUpdate,
) -> Any:
    """
    Update an annotation.
    """
    item = crudAnnotation.annotations.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Annotation not found")
    item = crudAnnotation.annotations.update(db=db, db_obj=item, obj_in=annotation_in)
    return item