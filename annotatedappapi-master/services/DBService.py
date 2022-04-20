from databases.Databases import AccessDB
from models.Activity import Activity


class DBService:

    def __init__(self, accessDB: AccessDB):
        self.accessDB = accessDB

    def createAnnotation(self, annotation: dict):
        """
        Create a new annotation from the AccessDB.
        """
        try :
            self.accessDB.createAnnotation(annotation)
        except Exception as e:
            print(e)

    def readAnnotation(self, id: int):
        """
        Get an annotation from the AccessDB.
        """
        try :
            return self.accessDB.readAnnotation(id)
        except Exception as e:
            print(e)

    def updateAnnotation(self, annotation: dict):
        """
        Update an annotation from the AccessDB.
        """
        try :
            self.accessDB.updateAnnotation(annotation)
        except Exception as e:
            print(e)
        
    def deleteAnnotation(self, annotation: dict):
        """
        Delete an annotation from the AccessDB.
        """
        try :
            self.accessDB.deleteAnnotation(annotation)
        except Exception as e:
            print(e)

    def getAnnotationsOfADay(self, date):
        """
        Access all the annotation events of a day
        """
        try :
            return self.accessDB.getAllByDay(self, date.now())
        except Exception as e:
            print(e)

    def getAllActivity(self):
        """
        Get all activity from the AccessDB.
        """
        try :
            activities = []
            for activity in self.accessDB.getAllActivity():
                activities.append(activity)
            return activities
        except Exception as e:
            print(e)
    
    def createActivity(self, activity: Activity):
        """
        Create an activity from the AccessDB.
        """
        try :
            return self.accessDB.createActivity(activity)
        except Exception as e:
            print(e)

    def deleteActivity(self, label: str):
        """
        Delete an activity from the AccessDB.
        """
        try :
            # Probleme : les databases ont besoin de l'activité pour supprimer, mais seulement le label est spécifié.
            pass
        except Exception as e:
            print(e)
        

    