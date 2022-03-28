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