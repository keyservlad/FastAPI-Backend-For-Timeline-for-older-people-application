from datetime import datetime, time
from typing import Optional

from pydantic import BaseModel


# Shared properties
class AnnotationsBase(BaseModel):
    id:Optional[int] = 0
    home: Optional[str] = None
    room: Optional[str] = None
    start: Optional[datetime] = "2008-09-15T15:53:00+05:00"
    end: Optional[datetime] = "2008-09-15T15:53:00+05:00"
    activity_type: Optional[str] = None
    status: Optional[str] = None

# Properties to receive via API on creation
class AnnotationsCreate(AnnotationsBase):
    home: str
    room:str
    start:datetime
    end:datetime
    activity_type:str
    status:str
    
    class Config:
        orm_mode = True

# Properties to receive via API on update
class AnnotationsUpdate(AnnotationsBase):
    home: str
    room:str
    start:datetime
    end:datetime
    activity_type:str
    status:str
    
    class Config:
        orm_mode = True