from fastapi import APIRouter
from fastapi import HTTPException
from sqlalchemy import null
from annotate import Annotate
from annotate_query_services import AnnotateQueryService
from Activity import Activity

router = APIRouter()
service = AnnotateQueryService()



# Obtenir la liste des annotations
@router.get('/annotations')
def getAnnotations():
    try:
        return null
    except IndexError:
        raise HTTPException(status_code=404, detail="No annotation existing ")


# Ajouter une annotation
@router.post('/addAnnotation', status_code=201)
def addAnnotation(annotation: Annotate):
    return null


# Modifier une annotation
@router.put('/modifyAnnotation/id/{id}')
def modifyAnnotation(id: int):
    return null


# Delete une annotation
@router.delete('/deleteAnnotation/id/{id}')
def deleteAnnotation(id: int):
    return null


# Ajouter un type d'activité
@router.post('/addActivity', status_code=201)
def addActivity(activity: Activity):
    return null



# Obtenir la liste des activités possibles
@router.get('/activities')
def getActivities():
    try:
        return null
    except IndexError:
        raise HTTPException(status_code=404, detail="No activity existing")


# Delete un type d'activité
@router.delete('/deleteActivity/id/{id}')
def deleteActivity(id: int):
    return null
