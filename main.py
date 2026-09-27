from fastapi import FastAPI

from app.database import Base, engine
from app.router.noteendpoints import router as note_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Database Notes API")
app.include_router(note_router)
