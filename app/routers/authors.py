# app/routers/authors.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app import crud
from app.database import get_db

router = APIRouter(prefix="/authors", tags=["authors"])

@router.post("/", response_model=schemas.AuthorRead)
def create_author(author_in: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db, author_in)

@router.get("/", response_model=list[schemas.AuthorRead])
def list_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_authors(db, skip, limit)
