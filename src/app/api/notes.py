from app.api import crud
from app.api.models import NoteDB, NoteSchema
from app.db import get_db
from fastapi import APIRouter, HTTPException, Path, Depends
from typing import List
from datetime import datetime as dt
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=NoteDB, status_code=201)
async def create_note(payload: NoteSchema, db=Depends(get_db)):
    object_id = await crud.post(payload, db)
    created_date = dt.now().strftime("%Y-%m-%d %H:%M")
    response_object = {
        "id": object_id,
        "title": payload.title,
        "description": payload.description,
        "completed": payload.completed,
        "created_date": created_date,
    }
    return response_object


@router.get("/{note_id}/", response_model=NoteDB)
async def read_note(note_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    note = await crud.get(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.get("/", response_model=List[NoteDB])
async def read_all_notes(db=Depends(get_db)):
    return await crud.get_all(db)


@router.put("/{note_id}/", response_model=NoteDB)
async def update_note(
    payload: NoteSchema, note_id: int = Path(..., gt=0), db: Session = Depends(get_db)
):
    note = await crud.get(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    object_id = await crud.put(db, note_id, payload)
    response_object = {
        "id": object_id,
        "title": payload.title,
        "description": payload.description,
        "completed": payload.completed,
    }
    return response_object


# DELETE route
@router.delete("/{note_id}/", response_model=NoteDB)
async def delete_note(note_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    note = await crud.get(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    await crud.delete(db, note_id)

    return note


@router.get("/completed/{complete_status}/", response_model=List[NoteDB])
async def read_notes_by_complete_status(complete_status: bool = False, db=Depends(get_db)):
    return await crud.get_notes_by_complete_status(db, complete_status)


@router.get("/title/{title}/", response_model=List[NoteDB])
async def read_note_by_title(title: str, db=Depends(get_db)):
    return await crud.get_by_title(db, title)


@router.get("/description/{description}/", response_model=List[NoteDB])
async def read_note_by_description(description: str, db=Depends(get_db)):
    return await crud.get_by_description(db, description)


@router.get("/date/{created_date}/", response_model=List[NoteDB])
async def read_note_by_date(created_date: str, db=Depends(get_db)):
    return await crud.get_by_date(db, created_date)

@router.delete("/", response_model=str)
async def delete_all_notes(db=Depends(get_db)):
    return await crud.delete_all(db)