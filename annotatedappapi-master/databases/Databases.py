

from ast import Str
from cProfile import label
import psycopg2
import mysql.connector
import csv
import datetime
from abc import ABC, abstractmethod
from pydantic.dataclasses import dataclass
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi.encoders import jsonable_encoder
from databases.ORM import Annotations, Activities
from models.Activity import Activity
from models.annotate import Annotate
import datetime as DT
from schemas.annotate_schemas import *
from typing import TypeVar
from pydantic import BaseModel
import pymongo
from dateutil.tz import tzlocal, tzoffset
from pymongo import MongoClient
from pymongo.command_cursor import CommandCursor
from pymongo.errors import OperationFailure
from pymongo.collection import Collection
import pymongo


UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class AccessDB(ABC):

    def __init__(self, database: str, host: str = None, port: str = None, username: str = None, password: str = None):
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

    @abstractmethod
    def getAllByDay(self, date: datetime.datetime):
        """
        Get all annotations in the database, by date
        """
        pass

    @abstractmethod
    def createActivity(self, activity: Activity):
        """
        Create an activity in the database.
        """
        pass

    @abstractmethod
    def deleteActivity(self, activity: Activity):
        """
        Delete an activity in the database.
        """
        pass

    @abstractmethod
    def getAllActivity(self):
        """
        Get all activities.
        """
        pass

class MongoDB(AccessDB):
    def connect(self):
        client = pymongo.MongoClient("mongodb+srv://test1:gntestyes-F4f756@cluster0.rqf6z.mongodb.net/labellingapp?retryWrites=true&w=majority")


        self.annotate: Collection = client.home.annotate
        self.activity: Collection = client.home.activity

    def createAnnotation(self, annotation: Annotate):
        _id = self.collection_name.insert_one(dict(annotation))
        return annotates_serializer(self.annotate.find({"_id":_id.inserted_id}))

    def readAnnotation(self, id: int):
        pipeline = [
            {
                '$match': {'id': id}
            },
            {
                '$group': {
                    '_id': {'id': '$id', 'start': '$start', 'end': '$end', 'room': '$room', 'home': '$home', 'activity_type': '$activity_type', 'status': '$status'}
                }
            }
        ]
        try:
            cursor: CommandCursor = self.annotate.aggregate(pipeline)
            return (MongoDB.map_annotate(x) for x in cursor)
        except OperationFailure as ex:
            raise MongoDB(ex.details)

    def updateAnnotation(self, annotate: Annotate):
        home_entry  = self.collection_name.find_one({"id": annotate.id})
        if home_entry:
            self.collection_name.find_one_and_update({"id": annotate.id},{"$set":dict(annotate)})
            return annotate_serializer(self.collection_name.find_one({"id":id}))
        else:
            return self.insert_home_annotate(annotate)

    def deleteAnnotation(self, id: int):
        result = db.test.delete_one({'id': id})
        return result.deleted_count

    def createActivity(self, activity: Activity):
        _id = self.collection_name.insert_one(dict(activity))
        return annotates_serializer(self.annotate.find({"_id":_id.inserted_id}))

    def deleteActivity(self, activity: Activity):
        result = db.test.delete_one({'label': activity.label})
        return result.deleted_count

    def getAllActivity(self):
        """
        Get all activities.
        """
        return annotates_serializer(self.activity.find())

    def getAllByDay(self, date: datetime.datetime):
        dateOneMore = date + datetime.timedelta(days=1)
        return annotates_serializer(self.annotate.find({"start": { 
                          "$gte": date}
                         }, {"end": { "$lt": dateOneMore }}))
     

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
        val = (annotation.id, annotation.home, annotation.start, annotation.end,
               annotation.room, annotation.subject, annotation.status, )
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
        val = (annotation.home, start, end, annotation.room,
               annotation.subject, annotation.status, annotation.id, )

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

    def createActivity(self, activity: Activity):
        """
        Create an activity in the database.
        """
        mycursor = self.db_conn.cursor()
        sql = "INSERT INTO activity (label) VALUES (%s)"
        val = (activity.label, )
        mycursor.execute(sql, val)
        self.db_conn.commit()

    def getAllActivity(self):
        """
        Get all activity in the database.
        """
        mycursor = self.db_conn.cursor()
        sql = "SELECT * FROM activity"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        return myresult

    def deleteActivity(self, activity: Activity):
        """
        Delete an activity from the database.
        """
        mycursor = self.db_conn.cursor()
        sql = "DELETE FROM activity WHERE label = %s"
        param = (activity.label, )
        mycursor.execute(sql, param)
        self.db_conn.commit()
    
    def getAllByDay(self, date: datetime.datetime):
        pass

class PostgreSQL(AccessDB):

    def connect(self):
        """
        Establish a connection with the PostgreSQL database using psycopg2.
        output postgresql connection
        """
        self.db: Session = self.get_db()
        pg = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.username,
            password=self.password
        )
        return pg

    def get_db(self):
        try:
            engine = create_engine(
                f"postgresql://{self.username}:{self.password}@{self.host}/{self.database}", pool_pre_ping=True)
            db = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            return db()
        finally:
            db().close()

    def createAnnotation(self, annotation: Annotate):
        """
        Create an annotation in the database.
        """
        # Implementation goes here.

        obj = self.db.query(Annotations).order_by(Annotations.id.desc()).first()
        if obj:
            annotation.id = obj.id+1
        else:
            annotation.id = 1
        
        db_obj = Annotations(
            id=annotation.id,
            home=annotation.home,
            room=annotation.room,
            start=annotation.start,
            end=annotation.end,
            activity_type=annotation.activity_type,
            status=annotation.status
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        self.db.close()
        return db_obj

    def readAnnotation(self, id: int):
        """
        Read an annotation from the database, given its id.
        """
        # Implementation goes here.
        item = self.db.query(Annotations).filter(Annotations.id == id).first()
        return item

    def updateAnnotation(self, annotation: Annotate):
        """
        Update an annotation in the database, given its id and the new annotation
        """
        # Implementation goes here.

        item = self.db.query(Annotations).filter(
            Annotations.id == annotation.id).first()
        if not item:
            print("Annotation not found")
            return
        item.id=annotation.id,
        item.home=annotation.home,
        item.room=annotation.room,
        item.start=annotation.start,
        item.end=annotation.end,
        item.activity_type=annotation.activity_type,
        item.status=annotation.status
        self.db.commit()
        return item.to_annotate()

    def deleteAnnotation(self, id: int):
        """
        Delete an annotation in the database, given its id.
        """
        # Implementation goes here.
        item = self.db.query(Annotations).filter(Annotations.id == id).first()
        if not item:
            print("Annotation not found")
            return
        obj = self.db.query(Annotations).get(id)
        self.db.delete(obj)
        self.db.commit()
        return obj.to_annotate()
    
    def createActivity(self, activity: Activity):
        """
        Create an activity in the database.
        """
        item = self.db.query(Activities).filter(Activities.label == activity.label).first()
        if item:
            return
        db_obj = Activities(
            label=activity.label
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj.to_activity()

    def deleteActivity(self, activity: Activity):
        """
        Delete an activity in the database.
        """
        item = self.db.query(Activities).filter(Activities.label == activity.label).first()
        if not item:
            print("Activity not found")
            return
        obj = self.db.query(Activities).get(activity.label)
        self.db.delete(obj)
        self.db.commit()
        return obj.to_activity()

    def getAllActivity(self):
        """
        Get all activities.
        """
        obj=self.db.query(Activities).all()
        return obj

    def getAllByDay(self, date: datetime.datetime):
        dateOneMore = date + datetime.timedelta(days=1)
        items = self.db.query(Annotations).filter(and_(Annotations.start > date, Annotations.end < dateOneMore)).all()
        self.db.close()
        return items

class CSV(AccessDB):

    def connect(self):
        """
        Basically just returns the database name, which should be the .csv file relative path.
        output : database name as string.
        """
        path = self.database+".csv"
        #path = 'databases/' + self.database + '.csv'
        print('path to csv database: ', path)
        # set fieldnames for csv file
      #  csvreader = csv.DictReader(open("events.csv"))
       # self.fieldnames = csvreader.fieldnames
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
            print(annotation.activity_type)
            writer.writerow({'id': annotation.id, 'start': annotation.start, 'end': annotation.end, 'room': annotation.room,
                            'subject': annotation.subject, 'home': annotation.home, 'activity_type': annotation.activity_type, 'status': annotation.status})
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
            print('Cannot update annotation, because annotation with id ',
                  annotation.id,  ' not exist')
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

    def createActivity(self, label: str):
        """
        Create an activity in the database.
        """
        pass

    def deleteActivity(self, label: str):
        """
        Delete an activity in the database, given its label.
        """
        pass

    def getAllActivity(self):
        """
        Get all activities.
        """
        pass

    def getAllByDay(self, date: datetime.datetime):
        all_annotate = []
        with open(self.db_conn, 'r') as csvfile:
            datareader = csv.DictReader(csvfile, delimiter=',')
            for row in datareader:
                row_date = row["start"].split(" ")[0]
                if(date == row_date):
                    all_annotate.append(Annotate(id=int(row['id']), start=row['start'], end=row['end'], room=row['room'], subject=row['subject'], home=row['home'], activity_type="", status=""))
            return all_annotate

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
    _input = input(
        "Select a database to use: \n 0. PostgreSQL \n 1. MySQL \n 2. CSV \n")
    try:
        db = databases[int(_input)]
    except Exception as e:
        print("Invalid input")
        print(e)
        return select_db(databases)
    return db


    return jsonable_encoder(annotateList)


        

