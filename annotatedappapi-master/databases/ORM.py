from sqlalchemy import  Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from typing import Any
from models.annotate import Annotate
from models.Activity import Activity


@as_declarative()
class Base:
    id: Any
    __name__: str
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

class Annotations(Base):
    id = Column(Integer, primary_key=True, index=True)
    home=  Column(String, index=False)
    room = Column(String, index=False)
    start= Column(DateTime, index=False)
    end=Column(DateTime, index=False)
    activity_type= Column(String, index=False)
    status= Column(String, index=False)

    def to_annotate(self):
        return Annotate(
            id=self.id,
            start=self.start,
            end=self.end,
            room=self.room,
            home=self.home,
            activity_type=self.activity_type,
            status=self.status,
        )

class Activities(Base):
    label = Column(String, primary_key=True, index=True)

    def to_activity(self):
        return Activity(
            label = self.label,
        )