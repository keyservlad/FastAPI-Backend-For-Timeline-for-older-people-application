import datetime
from urllib.parse import quote_plus
from typing import Optional, List, Tuple
from enum import Enum

from dateutil.tz import tzlocal, tzoffset
from pymongo import MongoClient
from pymongo.command_cursor import CommandCursor
from pymongo.errors import OperationFailure
from pymongo.collection import Collection

from config.db import Settings
from models.annotate import Annotate
from schemas.annotate_schemas import annotate_serializer, annotates_serializer
class ConfigurationException(Exception):
    def __init__(self, name: str):
        self.name = name


class AnnotateQueryService:
    def __init__(self):
        client = MongoClient(
            f'mongodb://{Settings().mongo_username}'
            f':{quote_plus(Settings().mongo_password)}'
            f'@{Settings().mongo_host}'
            f':{Settings().mongo_port}/admin')

        self.annotate: Collection = client.labellingapp.annotateapp
        self.collection_name = client.labellingapp["annotateapp"]

    def get_home_annotate(self, home):
        pipeline = [
            {
                '$match': {'home': home}
            },
            {
                '$group': {
                    '_id': {'home': '$home', 'item': '$item', 'start': '$start', 'end': '$end', 'answer': '$answer'},
                    'observations_count': {'$sum': 1},
                    'first_observation_date': {'$min': '$sentAt'},
                    'last_observation_date': {'$max': '$sentAt'}
                }
            }
        ]

        try:
            cursor: CommandCursor = self.annotate.aggregate(pipeline)
            return (AnnotateQueryService.map_annotate(x) for x in cursor)
        except OperationFailure as ex:
            raise ConfigurationException(ex.details)


    def insert_home_annotate(self, annotation):
        _id = self.collection_name.insert_one(dict(annotation))
        return annotates_serializer(self.annotate.find({"_id":_id.inserted_id}))

    def update_home_annotate(self, home, start, end, annoate):

        home_entry  = self.collection_name.find_one({"home": home, "start": start, "end":end})
        if home_entry:
            self.collection_name.find_one_and_update({"home": home},{"$set":dict(annoate)})
            return annotate_serializer(self.collection_name.find_one({"home":home}))
        else:
            return self.insert_home_annotate(annoate)


    @staticmethod
    def add_tz_info(value: datetime.datetime):
        return value.replace(tzinfo=tzlocal()).astimezone(tzoffset(None, 0))

    @staticmethod
    def map_annotate(annotate):
        return Annotate(
            annotate['_id']['home'],
            annotate['_id']['item'],
            annotate['_id']['start'],
            annotate['_id']['end'],
            annotate['_id']['answer'],
            annotate['observations_count'],
            AnnotateQueryService.add_tz_info(annotate['first_observation_date']),
            AnnotateQueryService.add_tz_info(annotate['last_observation_date']))

