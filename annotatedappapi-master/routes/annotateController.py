from aifc import Error
import os
from dotenv import load_dotenv
from fastapi import Body, APIRouter
from fastapi import HTTPException
from sqlalchemy import null
from models.annotate import Annotate
from services.DBService import DBService
from databases.Databases import AccessDB, PostgreSQL
from models.Activity import Activity

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
@router.get('/annotations')
def getAnnotations(payload: dict = Body(...)):
    try:
        
    except Error:
        raise HTTPException(status_code=404, detail="No annotation existing ")

#enlever
# Ajouter une annotation
@router.post('/annotations', status_code=201)
def addAnnotation(annotation: Annotate):
    try:
        return null
    except Error:
        raise HTTPException(status_code=404, detail="can't add annotation")


# Modifier une annotation
@router.put('/annotations/{id}')
def modifyAnnotation(id: int):
    try:
        return null
    except Error:
        raise HTTPException(status_code=404, detail="Can't modify annotation")


# Delete une annotation
@router.delete('/annotations/{id}')
def deleteAnnotation(id: int):
    try:
        return null
    except Error:
        raise HTTPException(status_code=404, detail="Can't delete annotation")


# Ajouter un type d'activité
@router.post('/activities', status_code=201)
def addActivity(activity: Activity):
    try:
        return null
    except Error:
        raise HTTPException(status_code=404, detail="Can't add an activity")



# Obtenir la liste des activités possibles
@router.get('/activities')
def getActivities():
    try:
        return null
    except Error:
        raise HTTPException(status_code=404, detail="No activity existing")


# Delete un type d'activité
@router.delete('/activities/{label}')
def deleteActivity(label: str):
    try:
        return null
    except Error:
        raise HTTPException(status_code=404, detail="Can't delete this activity")
