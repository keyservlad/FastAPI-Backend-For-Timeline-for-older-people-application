from typing import Optional

from pydantic import BaseModel


# Shared properties
class AnnotationsBase(BaseModel):
    home: Optional[str] = None
    room: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None
    activity_type: Optional[str] = None
    status: Optional[str] = None

# Properties to receive via API on creation
class AnnotationsCreate(AnnotationsBase):
    home: str
    room:str
    start:str
    end:str
    activity_type:str
    status:str