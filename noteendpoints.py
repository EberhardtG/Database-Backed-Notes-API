"""
WHY:
The notes router provides the core CRUD functionality for the Note API. It
connects validated Pydantic schemas with the SQLAlchemy database model, ensuring
that all note operations are safe, predictable, and fully aligned with the
assignment requirements. Each endpoint is designed to be simple, explicit, and
easy to extend as the application grows.

DESIGN:
1. The POST /notes endpoint accepts a NoteCreate schema, ensuring that all
   incoming data is validated before being persisted. A new Note ORM instance is
   created, committed, and refreshed so that database-generated fields such as
   created_at are included in the response.

2. The GET /notes endpoint supports optional filtering by category and is_pinned.
   These filters allow clients to retrieve only the notes they care about while
   still supporting full list retrieval. Results are ordered by created_at in
   descending order to show the most recent notes first.

3. The GET /notes/{note_id} endpoint retrieves a single note by its primary key.
   If the note does not exist, a clear 404 error is returned. This ensures
   predictable lookup behavior and prevents ambiguous responses.

4. The DELETE /notes/{note_id} endpoint removes a note from the database and
   returns a 204 No Content response. It also performs a 404 check to ensure
   that only existing notes can be deleted.

5. All endpoints use NoteResponse as the response model, allowing Pydantic to
   serialize SQLAlchemy ORM objects cleanly using from_attributes=True. This
   keeps the API output consistent and strongly typed.

Overall, this router provides a clean, validated, and database-backed interface
for managing notes. It demonstrates proper FastAPI patterns, strong schema
integration, and reliable SQLAlchemy usage.
"""



from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import Note, get_db
from app.schemas.notecreate import NoteCreate
from app.schemas.noteresponse import NoteResponse

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
	db_note = Note(**note.model_dump())
	db.add(db_note)
	db.commit()
	db.refresh(db_note)
	return db_note


@router.get("", response_model=list[NoteResponse])
def list_notes(
	category: Optional[str] = None,
	is_pinned: Optional[bool] = None,
	db: Session = Depends(get_db),
):
	query = db.query(Note)
	if category is not None:
		query = query.filter(Note.category == category)
	if is_pinned is not None:
		query = query.filter(Note.is_pinned == is_pinned)
	return query.order_by(Note.created_at.desc()).all()


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
	note = db.query(Note).filter(Note.id == note_id).first()
	if note is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
	return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: Session = Depends(get_db)):
	note = db.query(Note).filter(Note.id == note_id).first()
	if note is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
	db.delete(note)
	db.commit()
	return Response(status_code=status.HTTP_204_NO_CONTENT)