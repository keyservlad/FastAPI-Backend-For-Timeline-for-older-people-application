from fastapi import APIRouter
from fastapi import HTTPException
from sqlalchemy import null
from annotate import Annotate
from annotate_query_services import AnnotateQueryService
from Activity import Activity


router = APIRouter()
service = AnnotateQueryService()

@router.get('/annotations/id/{id}')
def getAnnotation(id: int):
    try:
        return null
    except IndexError:
        raise HTTPException(status_code=404, detail="No annotation existing with this id")


@router.post('/addAnnotation', status_code=201)
def addAnnotation(annotation: Annotate):
    return null


@router.post('/addActivity', status_code=201)
def addActivity(activity: Activity):
    return null


@router.get('models/Activities.py/id/{id}')
def getActivity(id: int):
    try:
        return null
    except IndexError:
        raise HTTPException(status_code=404, detail="No activity existing with this id")


@router.delete('models/Activities.py/id/{id}')
def deleteActivity(id: int):
    return null
