from sqlalchemy import Boolean, Column, Integer, String,DateTime

from db.base_class import Base



class Annotations(Base):
    id = Column(Integer, primary_key=True, index=True)
    home=  Column(String, index=False)
    room = Column(String, index=False)
    start= Column(DateTime, index=False)
    end=Column(DateTime, index=False)
    activity_type= Column(String, index=False)
    status= Column(String, index=False)