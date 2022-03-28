from datetime import date, datetime
from pydantic import BaseModel

class AnnotateTest(BaseModel):
    home: str
    item: str
    start: int
    end: int
    answer: bool
    observationsCount: int
    firstObservationDate: datetime
    lastObservationDate: datetime
