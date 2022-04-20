from models.annotate import Annotate

def annotate_serializer(payload) -> Annotate:
    return Annotate(
        id=payload['id'],
        start=payload['start'],
        end=payload['end'],
        room=payload['room'],
        subject=payload['subject'],
        home=payload['home'],
        activity_type=payload['activity_type'],
        status=payload['status'],
    )
    

def annotates_serializer(annotates) -> list:
    return [annotate_serializer(annotate) for annotate in annotates]