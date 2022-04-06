from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.annotations import Annotations
from schemas.annotations import AnnotationsCreate,AnnotationsUpdate

class CRUDAnnotations(CRUDBase[Annotations,AnnotationsCreate,AnnotationsUpdate]):
    def get_by_id(self, db: Session, *, id: str) -> Optional[Annotations]:
        return db.query(Annotations).filter(Annotations.id == id).first()

    def create(self, db: Session, *, obj_in: AnnotationsCreate) -> Annotations:
        obj = db.query(Annotations).order_by(Annotations.id.desc()).first()
        if obj:
            obj_in.id=obj.id+1
        else:
            obj_in.id=1

        db_obj = Annotations(
            id=obj_in.id,
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