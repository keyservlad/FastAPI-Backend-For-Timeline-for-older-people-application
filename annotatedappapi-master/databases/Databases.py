
# ## MySQL credentials

# DB_NAME_SQL : sherbrooke_ift785_annotations
# HOST_SQL: mysql-sherbrooke.alwaysdata.net
# PORT_SQL : 3306
# USERNAME_SQL : 262938
# PASSWORD_SQL : Sr25qzz4@nf36mB

import psycopg2
import mysql.connector
import csv
import datetime
from abc import ABC, abstractmethod
from pydantic.dataclasses import dataclass
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from ORM import Annotations
# from models.annotate import Annotate

@dataclass
class Annotate:
    id: int
    start: datetime.datetime
    end: datetime.datetime
    room: str
    subject: str
    home: str
    activity_type:str
    status: str

class AccessDB(ABC):
    
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
    def updateAnnotation(self, annotation: Annotate):
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

class MySQL(AccessDB):

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
        end = annotation.end.strftime('%Y-%m-%d %H:%M:%S')
        start = annotation.start.strftime('%Y-%m-%d %H:%M:%S')
        mycursor = self.db_conn.cursor()
        sql = "INSERT INTO annotations (id, home,start,end,room,activity_type,status) VALUES (%s, %s,%s,%s,%s,%s,%s)"
        val = (annotation.id, annotation.home, annotation.start, annotation.end, annotation.room, annotation.subject, annotation.status, )
        mycursor.execute(sql, val)
        self.db_conn.commit()

    def readAnnotation(self, id: int):
        """
        Read an annotation from the database, given its id.
        """
        mycursor = self.db_conn.cursor()
        sql = "SELECT * FROM annotations WHERE id = %s"
        param = (id, )
        mycursor.execute(sql, param)
        myresult = mycursor.fetchone()
        return myresult
    
    def updateAnnotation(self, annotation: Annotate):
        """
        Update an annotation in the database, given its id and the new annotation
        """
        end = annotation.end.strftime('%Y-%m-%d %H:%M:%S')
        start = annotation.start.strftime('%Y-%m-%d %H:%M:%S')
        mycursor = self.db_conn.cursor()
        sql = "UPDATE annotations SET home = %s, start = %s, end = %s, room = %s, activity_type = %s, status = %s WHERE id = %s"
        val = (annotation.home, start, end, annotation.room, annotation.subject, annotation.status, annotation.id, )
        
        mycursor.execute(sql, val)
        self.db_conn.commit()
        print(mycursor.rowcount, "record(s) affected")
          
    def deleteAnnotation(self, id: int):
        """
        Delete an annotation in the database, given its id.
        """
        mycursor = self.db_conn.cursor()
        sql = "DELETE FROM annotations WHERE id = %s"
        param = (id, )
        mycursor.execute(sql, param)
        self.db_conn.commit()

class PostgreSQL(AccessDB):

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

    def get_db(self):
        try:
            engine = create_engine(f"postgresql://{self.username}:{self.password}@{self.host}/{self.database}", pool_pre_ping=True)
            db = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            return db()
        finally:
            db().close()

    def createAnnotation(self, annotation: Annotate):
        """
        Create an annotation in the database.
        """
        # Implementation goes here.
        db: Session = self.get_db()
        obj = db.query(Annotations).order_by(Annotations.id.desc()).first()
        if obj:
            annotation.id=obj.id+1
        else:
            annotation.id=1

        db_obj = Annotations(
            id=annotation.id,
            home=annotation.home,
            room=annotation.room,
            start=annotation.start,
            end=annotation.end,
            activity_type=annotation.activity_type,
            status=annotation.status
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def readAnnotation(self, id: int):
        """
        Read an annotation from the database, given its id.
        """
        # Implementation goes here.
        db: Session = self.get_db()
        item = db.query(Annotations).filter(Annotations.id == id).first()
        return item
    
    def updateAnnotation(self, annotation: Annotate):
        """
        Update an annotation in the database, given its id and the new annotation
        """
        # Implementation goes here.
        db: Session = self.get_db()
        item =  db.query(Annotations).filter(Annotations.id == annotation.id).first()
        if not item:
            print("Annotation not found")
            return
        obj_data = jsonable_encoder(item)
        if isinstance(annotation, dict):
            update_data = annotation
        else:
            update_data = annotation.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(item, field, update_data[field])
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    
    def deleteAnnotation(self, id: int):
        """
        Delete an annotation in the database, given its id.
        """
        # Implementation goes here.
        db: Session = self.get_db()
        item =  db.query(Annotations).filter(Annotations.id == id).first()
        if not item:
            print("Annotation not found")
            return
        obj = db.query(Annotations).get(id)
        db.delete(obj)
        db.commit()
        return obj

class CSV(AccessDB):
        
    def connect(self):
        """
        Basically just returns the database name, which should be the .csv file relative path.
        output : database name as string.
        """
        
        path = 'databases/' + self.database + '.csv'
        print('path to csv database: ', path)
        # set fieldnames for csv file
        csvreader = csv.DictReader(open(path))
        self.fieldnames = csvreader.fieldnames
        return path

    def createAnnotation(self, annotation: Annotate):
        """
        Create an annotation in the database.
        output : 1 if annotation doesnt exist, annotation if it already exists
        """
        # Check if the annotation already exists by id
        if self.readAnnotation(annotation.id) is not None:
            print('Annotation already exists')
            return self.readAnnotation(annotation.id)

        with open(self.db_conn, mode='a+', newline='') as csv_file:
            # check if annotation is already in the database by id
            writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            writer.writerow({'id': annotation.id, 'start': annotation.start, 'end': annotation.end, 'room': annotation.room, 'subject': annotation.subject, 'home': annotation.home, 'activity_type': annotation.activity_type ,'status': annotation.status})
            return 1

    def readAnnotation(self, id: int):
        """
        Read an annotation from the database, given its id.
        output = Annotation object if found, None if not found.
        """
        
        with open(self.db_conn, 'r') as csvfile:
            datareader = csv.DictReader(csvfile, delimiter=',')
            for row in datareader:
                if int(row['id']) == id:
                    return Annotate(id=int(row['id']), start=row['start'], end=row['end'], room=row['room'], subject=row['subject'], home=row['home'], activity_type=row['activity_type'], status=row['status'])
            return None
    
    def updateAnnotation(self, annotation: Annotate):
        """
        Update an annotation in the databas
        output = 1 if annotation is updated, 0 if not.
        """

        # delete annotation if exists
        if self.deleteAnnotation(annotation.id) == 1:
            # if dit has been delted, create new annotation
            self.createAnnotation(annotation)
            return 1
        else:
            print('Cannot update annotation, because annotation with id ', annotation.id,  ' not exist')
            return 0
    
    def deleteAnnotation(self, id: int):
        """
        Delete an annotation in the database, given its id.
        output = 1 if annotation is deleted, 0 if not.
        """
        # check if annotation exists
        if self.readAnnotation(id) == None:
            print('Annotation does not exist')
            return 0

        # Add rows to a list, excluding the row with the id that was passed in.
        kept_rows = []
        with open(self.db_conn, mode='r+', newline='') as csvfile:
            datareader = csv.DictReader(csvfile, delimiter=',')
            for row in datareader:
                if int(row['id']) != id:
                    kept_rows.append(row)
        
        with open(self.db_conn, mode='w', newline='') as csvfile:
            datawriter = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            datawriter.writeheader()
            datawriter.writerows(kept_rows)
        return 1
        
def connect_databases(remote=True):

    if remote:
        postgresql = PostgreSQL(
            'sherbrooke_ift785_annotations', 
            'postgresql-sherbrooke.alwaysdata.net',
            '5432', 
            'sherbrooke',
            'Sr25qzz4nf36mB'
        )

        _mysql = MySQL(
           'sherbrooke_ift785_annotations',
           'mysql-sherbrooke.alwaysdata.net', 
           '3306', 
            '262938',
            'Sr25qzz4nf36mB'
        )

        # NOTE : CSV remove access is not implemented yet. It will search in the local filesystem.
        _csv = CSV('playground_events')

        return postgresql, _mysql, _csv
    
    else: 
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

        return postgresql, _mysql, _csv

def generate_test_data():
    db = CSV(database='playground_events')
    for i in range(1, 5):
        annotation = Annotate(
            id=i,
            start=datetime.datetime.now(),
            end=datetime.datetime.now(),
            room='exterior',
            subject='rest',
            home='openhabianpi03-60962692-0d0d-41a3-a62b-1eddccd2a088'
        )
        db.createAnnotation(annotation)

def select_db(databases):
    _input = input("Select a database to use: \n 0. PostgreSQL \n 1. MySQL \n 2. CSV \n")
    try:
        db = databases[int(_input)]
    except Exception as e:
        print("Invalid input")
        print(e)
        return select_db(databases)
    return db

if __name__ == '__main__':

    annotation1 = Annotate(
    id=101,
    start=datetime.datetime.now(),
    end=datetime.datetime.now(),
    room='exterior',
    subject='rest',
    home='openhabianpi03-60962692-0d0d-41a3-a62b-1eddccd2a088',
    activity_type='hygiene',
    status='test'
    )

    annotation2 = Annotate(
    id=102,
    start=datetime.datetime.now(),
    end=datetime.datetime.now(),
    room='interior',
    subject='rest',
    home='openhabianpi03-60962692-0d0d-41a3-a62b-1eddccd2a088',
    activity_type='entertainment',
    status='test'
    )

    databases = connect_databases(remote=True)
    while True:
        db: AccessDB = select_db(databases)
        print('Connected to database: ', type(db).__name__)

        # Test requests
        # create
        input('Press any key to add data')
        db.createAnnotation(annotation1)
        db.createAnnotation(annotation2)

        # read
        input('Press any key to read data')
        response = db.readAnnotation(annotation1.id)
        print(response)

        # update
        input('Press any key to update data')
        annotation2.status = 'updated'
        db.updateAnnotation(annotation2)

        # delete
        input('Press any key to delete data')
        db.deleteAnnotation(annotation1.id)

        input('Press any key to delete data')
        db.deleteAnnotation(annotation2.id)

