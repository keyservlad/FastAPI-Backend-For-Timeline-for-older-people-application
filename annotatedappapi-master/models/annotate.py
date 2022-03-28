from datetime import date, datetime
from pydantic.dataclasses import dataclass

@dataclass
class Annotate:
    home: str
    item: str
    start: int
    end: int
    answer: bool
    observationsCount: int
    firstObservationDate: datetime
    lastObservationDate: datetime


    #def __repr__(self):
    #    return f'<Annotate {self.home}:{self.item}:{self.start}:{self.end}:{self.answer}>'