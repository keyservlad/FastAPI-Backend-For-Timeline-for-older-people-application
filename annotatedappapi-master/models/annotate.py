from datetime import datetime
from pydantic import BaseModel

class Annotate(BaseModel):
    id: int = None
    start: datetime
    end: datetime
    room: str
    activity_type: str
    home: str
    status: str


    


    #def __repr__(self):
    #    return f'<Annotate {self.home}:{self.item}:{self.start}:{self.end}:{self.answer}>'