"""
WHY:
The Note model defines the database representation of notes stored in the
ContactBook API. Using SQLAlchemy 2.0's typed ORM ensures strong integration
with Pydantic v2, allowing NoteResponse to serialize ORM objects cleanly using
from_attributes=True. The model enforces all constraints required by the
assignment and guarantees that notes are stored consistently and safely.

DESIGN:
1. The model inherits from DeclarativeBase, providing a clean SQLAlchemy 2.0
   foundation and enabling typed ORM fields through Mapped and mapped_column.

2. The id field is an integer primary key, ensuring each note can be uniquely
   identified. SQLAlchemy automatically indexes primary keys, so no manual index
   is required.

3. The title field is a required string capped at 200 characters, matching the
   validation rules in the NoteCreate schema and preventing excessively long
   titles.

4. The content field uses a TEXT column, allowing long-form note content without
   artificial length limits. This aligns with the assignment requirement for a
   text field.

5. The category field is optional and capped at 50 characters, ensuring
   consistent categorization while allowing notes to exist without a category.

6. The is_pinned field is a boolean with a default value of False, supporting
   pinned-note functionality without requiring clients to specify the field.

7. The created_at field uses server_default=func.now(), ensuring that timestamps
   are generated automatically by the database at creation time. This guarantees
   accurate creation metadata and aligns with the NoteResponse schema.

Overall, this model provides a clean, typed, and fully validated database
representation of notes, ensuring strong compatibility with FastAPI, Pydantic,
and SQLAlchemy 2.0.
"""



from __future__ import annotations
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text, Boolean, DateTime, Integer, func


class Base(DeclarativeBase):
    pass


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str | None] = mapped_column(String(50), nullable=True)
    is_pinned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
