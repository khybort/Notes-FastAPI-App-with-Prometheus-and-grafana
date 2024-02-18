from app.api.models import NoteSchema
from app.db import notes, database
from datetime import datetime as dt
from sqlalchemy.orm import Session


async def post(payload: NoteSchema, db: Session):
    created_date = dt.now().strftime("%Y-%m-%d %H:%M")
    note = notes.insert().values(title=payload.title,
                                  description=payload.description, completed=payload.completed,
                                  created_date=created_date)
    result = db.execute(note)
    note_id = result.inserted_primary_key[0]
    db.commit()
    return note_id


async def get(db: Session, note_id: int):
    return db.query(notes).filter_by(id=note_id).first()


async def get_all(db):
    return db.query(notes).all()


async def put(db: Session, note_id: int, payload=NoteSchema):
    created_date = dt.now().strftime("%Y-%m-%d %H:%M")
    payload.created_date = created_date
    db.query(notes).filter_by(id=note_id).update(payload.to_dict())
    db.commit()
    return note_id


async def delete(db: Session, note_id: int):
    result = db.query(notes).filter_by(id=note_id).delete()
    db.commit()
    return result


async def get_notes_by_complete_status(db: Session, complete_status: bool = False):
    return db.query(notes).filter_by(completed=f"{complete_status}").all()



async def get_by_title(db: Session, title: str):
    return db.query(notes).filter_by(title=title).all()


async def get_by_description(db: Session, description: str):
    return db.query(notes).filter_by(description=description).all()


async def get_by_date(db: Session, created_date: str):
    return db.query(notes).filter_by(created_date=created_date).all()


async def delete_all(db: Session):
    result = db.query(notes).delete()
    if result:
        db.commit()
        return "Deleted"
    return "Can't delete"