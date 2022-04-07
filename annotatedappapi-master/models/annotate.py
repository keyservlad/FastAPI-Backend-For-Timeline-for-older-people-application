from datetime import date, datetime
from pydantic.dataclasses import dataclass

@dataclass
class Annotate:
    id: int
    start: datetime
    end: datetime
    room: str
    subject: str
    home: str
    status: str


    #def __repr__(self):
    #    return f'<Annotate {self.home}:{self.item}:{self.start}:{self.end}:{self.answer}>'