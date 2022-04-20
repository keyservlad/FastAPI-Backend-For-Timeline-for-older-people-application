from databases.Databases import AccessDB
from models.Activity import Activity
import datetime



class DBService:

    def __init__(self, accessDB: AccessDB):
        self.accessDB = accessDB

    def createAnnotation(self, annotation: dict):
        """
        Create a new annotation from the AccessDB.
        """
        try :
            return self.accessDB.createAnnotation(annotation)
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
            return self.accessDB.updateAnnotation(annotation)
        except Exception as e:
            print(e)
        
    def deleteAnnotation(self, id: int):
        """
        Delete an annotation from the AccessDB.
        """
        try :
            return self.accessDB.deleteAnnotation(id)
        except Exception as e:
            print(e)

    def getAnnotationsOfADay(self, date: str):
        """
        Access all the annotation events of a day
        """
        try :
            dateParsed = datetime.datetime.strptime(date, "%Y-%m-%d")
            week_ago = dateParsed - datetime.timedelta(days=7)
            return self.accessDB.getAllByDay(week_ago)
        except Exception as e:
            print(e)

    def getAllActivity(self):
        """
        Get all activity from the AccessDB.
        """
        try :
            return self.accessDB.getAllActivity()
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
            activity = Activity(
                label=label,
            )
            return self.accessDB.deleteActivity(activity)
        except Exception as e:
            print(e)
        

    