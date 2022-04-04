from __future__ import annotations
from turtle import home

from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.annotations import Annotations
from schemas.annotations import AnnotationsCreate

class CRUDAnnotations(CRUDBase[Annotations,AnnotationsCreate]):
    def create(self, db: Session, *, obj_in: AnnotationsCreate) -> Annotations:
        db_obj = Annotations(
            home=obj_in.home,
            room=obj_in.room,
            start=obj_in.start,
            end=obj_in.end,
            activity_type=obj_in.activity_type,
            status=obj_in.status
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

annotations = CRUDAnnotations(Annotations)