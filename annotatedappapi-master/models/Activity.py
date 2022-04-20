from pydantic import BaseModel

@dataclass
class Activity(BaseModel):
    label: str