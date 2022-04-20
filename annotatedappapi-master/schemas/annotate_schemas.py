from models.annotate import Annotate

def annotate_serializer_json(payload) -> Annotate:
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
    
def annotate_serializer(annotate) -> dict:

    return{
        "id": str(annotate["_id"]),
        "home": annotate["home"],
        "item": annotate["item"],
        "start": annotate["start"],
        "end": annotate["end"],
        "answer": annotate["answer"],
        "observationsCount": annotate["observationsCount"],
        "firstObservationDate": annotate["firstObservationDate"],
        "lastObservationDate": annotate["lastObservationDate"]
    }


def annotates_serializer(annotates) -> list:
    return [annotate_serializer(annotate) for annotate in annotates]