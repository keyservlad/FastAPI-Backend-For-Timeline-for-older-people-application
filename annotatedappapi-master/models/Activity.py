from pydantic import BaseModel


class Activity(BaseModel):

    activity_name: str
    id: int