"""
WHY:
The NoteCreate schema defines the required structure and validation rules for
creating new notes in the Note API. It ensures that incoming data is clean,
correctly typed, and aligned with the SQLAlchemy model before being persisted to
the database.

DESIGN:
1. The title field is required and capped at 200 characters to match the database
   column constraint and prevent excessively long note titles.

2. The content field is required but intentionally left without a max_length
   because the database uses a TEXT column, allowing long-form note content
   without artificial limits.

3. The category field is optional and capped at 50 characters, matching the
   database constraint and ensuring consistent categorization.

4. The is_pinned field defaults to False, allowing clients to omit it while still
   supporting pinned-note functionality.

Overall, this schema ensures that all note creation requests are validated,
consistent with the database model, and safe to store.
"""



from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class NoteCreate(BaseModel):
   title: str = Field(min_length=1, max_length=200)
   content: str = Field(min_length=1)
   category:Optional[str] | None=Field(default=None, max_length=50)
   is_pinned: bool =Field(default=False)