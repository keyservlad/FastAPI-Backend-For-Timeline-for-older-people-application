from datetime import date, datetime
from pydantic.dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class Annotate(BaseModel):
    id: int
    start: datetime
    end: datetime
    room: str
    subject: str
    home: str
    status: str


    


    #def __repr__(self):
    #    return f'<Annotate {self.home}:{self.item}:{self.start}:{self.end}:{self.answer}>'