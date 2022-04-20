from pydantic import BaseModel
from pydantic.dataclasses import dataclass

class Activity(BaseModel):
    label: str