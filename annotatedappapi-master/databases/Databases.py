
# ## MySQL credentials

# DB_NAME_SQL : sherbrooke_ift785_annotations
# HOST_SQL: mysql-sherbrooke.alwaysdata.net
# PORT_SQL : 3306
# USERNAME_SQL : 262938
# PASSWORD_SQL : Sr25qzz4@nf36mB

import string
import psycopg2
import mysql.connector
import csv
import datetime
from abc import ABC, abstractmethod
from pydantic.dataclasses import dataclass

@dataclass
class Annotate:
    id: int
    start: datetime.datetime
    end: datetime.datetime
    room: str
    subject: str
    home: str

class Database(ABC):
    
    def __init__(self, database: str, host: str = None, port: str=None, username:str=None, password:str=None):
        self.database = database
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db_conn = self.connect()

    @abstractmethod
    def connect(self):
        """
        Attempt to 'connect' to the concrete database. 
        NOTE : The word 'connect' is a language abuse (ex : it doesnt make sense to 'connect' a csv file.)
        See concrete implementation for a better definition.
        """
        pass

    @abstractmethod
    def createAnnotation(self, annotation: Annotate):
        """
        Create an annotation in the database.
        """
        pass

    @abstractmethod
    def readAnnotation(self, id: int):
        """
        Read an annotation from the database, given its id.
        """
        pass
    
    @abstractmethod
    def updateAnnotation(self, id:int, annotation: Annotate):
        """
        Update an annotation in the database, given its id and the new annotation
        """
        pass
    
    @abstractmethod
    def deleteAnnotation(self, id: int):
        """
        Delete an annotation in the database, given its id.
        """
        pass


class MySQL(Database):

    def connect(self):
        """
        Establish a connection with the MySQL database using mysql.connector.
        output : mysql connection
        """
        _mysql = mysql.connector.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.username,
            password=self.password
        )
        print(_mysql)
        return _mysql

    def createAnnotation(self, annotation: Annotate):
        """
        Create an annotation in the database.
        """
        # Implementation goes here.
        pass

    def readAnnotation(self, id: int):
        """
        Read an annotation from the database, given its id.
        """
        # Implementation goes here.
        pass
    
    def updateAnnotation(self, id:int, annotation: Annotate):
        """
        Update an annotation in the database, given its id and the new annotation
        """
        # Implementation goes here.
        pass
    
    def deleteAnnotation(self, id: int):
        """
        Delete an annotation in the database, given its id.
        """
        # Implementation goes here.
        pass


class PostgreSQL(Database):

    def connect(self):
        """
        Establish a connection with the PostgreSQL database using psycopg2.
        output postgresql connection
        """
        pg = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.username,
            password=self.password
        )
        print(pg)
        return pg

    def createAnnotation(self, annotation: Annotate):
        """
        Create an annotation in the database.
        """
        # Implementation goes here.
        pass

    def readAnnotation(self, id: int):
        """
        Read an annotation from the database, given its id.
        """
        # Implementation goes here.
        pass
    
    def updateAnnotation(self, id:int, annotation: Annotate):
        """
        Update an annotation in the database, given its id and the new annotation
        """
        # Implementation goes here.
        pass
    
    def deleteAnnotation(self, id: int):
        """
        Delete an annotation in the database, given its id.
        """
        # Implementation goes here.
        pass

class CSV(Database):
        
    
    def connect(self):
        """
        Baically just returns the database name, which should be the .csv file relative path.
        output : database name as string.
        """
        path = 'annotatedappapi-master/databases/' + self.database + '.csv'
        print('path to csv database: ', path)
        # set fieldnames for csv file
        csvreader = csv.DictReader(open(path))
        return path

    def createAnnotation(self, annotation: Annotate):
        """
        Create an annotation in the database.
        """
        # Check if the annotation already exists by id
        if self.readAnnotation(annotation.id) is not None:
            print('Annotation already exists')
            return    

        with open(self.db_conn, mode='a+', newline='') as csv_file:
            # check if annotation is already in the database by id
            writer = csv.DictWriter(csv_file)
            writer.writerow({'id': annotation.id, 'start': annotation.start, 'end': annotation.end, 'measure': 'activity', 'room': annotation.room, 'subject': annotation.subject, 'home': annotation.home})

    def readAnnotation(self, id: int):
        """
        Read an annotation from the database, given its id.
        output = Annotation object if found, None if not found.
        """
        #self closing operation
        with open(self.db_conn, 'r') as csvfile:
            datareader = csv.DictReader(csvfile, delimiter=',')
            for row in datareader:
                if int(row['id']) == id:
                    print('Row found', row)
                    annotation = Annotate(id=int(row['id']), start=row['start'], end=row['end'], room=row['room'], subject=row['subject'], home=row['home'])
                    print('annotation found: ', annotation)
                    return Annotate(id=int(row['id']), start=row['start'], end=row['end'], room=row['room'], subject=row['subject'], home=row['home'])
            return None
    
    def updateAnnotation(self, id:int, annotation: Annotate):
        """
        Update an annotation in the database, given its id and the new annotation
        """
        # Implementation goes here.
        pass
    
    def deleteAnnotation(self, id: int):
        """
        Delete an annotation in the database, given its id.
        """
        # Implementation goes here.
        pass


    
if __name__ == '__main__':
    
    annotation = Annotate(
        id=1,
        start=datetime.datetime.now(),
        end=datetime.datetime.now(),
        room='exterior',
        subject='rest',
        home='openhabianpi03-60962692-0d0d-41a3-a62b-1eddccd2a088'
    )

    db_connection = 'remote'
    if db_connection == 'local':
        
        postgresql = PostgreSQL(
            'ift785', 
            'localhost', 
            '5432', 
            'postgres', 
            'admin'
        )

        _mysql = MySQL(
            'ift785',
            'localhost', 
            '3306', 
            'mysql',
            'admin'
        )
        
        _csv = CSV('playground_events') 
    elif db_connection == 'remote':

        # postgresql = PostgreSQL(
        #     'sherbrooke_ift785_annotations', 
        #     'postgresql-sherbrooke.alwaysdata.net',
        #     '5432', 
        #     'sherbrooke',
        #     'Sr25qzz4nf36mB'
        # )

        # _mysql = MySQL(
        #     'sherbrooke_ift785_annotations',
        #     'mysql-sherbrooke.alwaysdata.net', 
        #     '3306', 
        #     '262938',
        #     'Sr25qzz4nf36mB'
        # )

        # NOTE : CSV remove access is not implemented yet. It will search in the local filesystem.
        _csv = CSV('playground_events') 

        _csv.createAnnotation(annotation)
        # _csv.readAnnotation(annotation.id)

