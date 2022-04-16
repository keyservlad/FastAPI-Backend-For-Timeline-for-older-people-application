from sqlalchemy import  Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from typing import Any

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

class Activity(Base):
    label = Column(String, primary_key=True, index=True)