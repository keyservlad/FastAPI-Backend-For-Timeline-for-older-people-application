from aifc import Error
import os
from dotenv import load_dotenv
from fastapi import Body, APIRouter
from fastapi import HTTPException
from sqlalchemy import null
from models.annotate import Annotate
from models.Activity import Activity

from services.DBService import DBService
from databases.Databases import AccessDB, PostgreSQL
from schemas.annotate_schemas import annotate_serializer


load_dotenv()
router = APIRouter()
accessDBTest : AccessDB = PostgreSQL(
            os.getenv("POSTGRES_DB"),
            os.getenv("POSTGRES_SERVER"),
            os.getenv("POSTGRES_PORT"),
            os.getenv("POSTGRES_USER"),
            os.getenv("POSTGRES_PASSWORD")
        )


service = DBService(accessDBTest)

#body -> {date: "jj/mm/aaaa"}

# Obtenir la liste des annotations
@router.get('/annotations/{date}')
def getAnnotations(date: str):
    try:
        return service.getAnnotationsOfADay(date)
    except Error:
        raise HTTPException(status_code=500, detail="Error retrieving annotations")

#enlever
# Ajouter une annotation
@router.post('/annotations', status_code=201)
def addAnnotation(annotation: Annotate):
    try:
        return service.createAnnotation(annotation)
    except Error:
        raise HTTPException(status_code=500, detail="can't add annotation")


# Modifier une annotation
@router.put('/annotations/{id}')
def modifyAnnotation(annotation: Annotate):
    try:
        return service.updateAnnotation(annotation)
    except Error:
        raise HTTPException(status_code=500, detail="Can't modify annotation")


# Delete une annotation
@router.delete('/annotations/{id}')
def deleteAnnotation(id: int):
    try:
        return service.deleteAnnotation(id)
    except Error:
        raise HTTPException(status_code=500, detail="Can't delete annotation")


# Ajouter un type d'activité
@router.post('/activities', status_code=201)
def addActivity(activity: Activity):
    try:
        return service.createActivity(activity)
    except Error:
        raise HTTPException(status_code=404, detail="Can't add an activity")



# Obtenir la liste des activités possibles
@router.get('/activities')
def getActivities():
    try:
        return service.getAllActivity()
    except Error:
        raise HTTPException(status_code=404, detail="No activity existing")


# Delete un type d'activité
@router.delete('/activities/{label}')
def deleteActivity(label: str):
    try:
        return service.deleteActivity(label)
    except Error:
        raise HTTPException(status_code=404, detail="Can't delete this activity")
