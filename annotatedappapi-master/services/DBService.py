from databases.Databases import AccessDB



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

    def readAnnotation(self, annotation: dict):
        """
        Get an annotation from the AccessDB.
        """
        try :
            return self.accessDB.readAnnotation(annotation)
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
            self.accessDB.getAllByDay(self, date)
        except Exception as e:
            print(e)
        

    