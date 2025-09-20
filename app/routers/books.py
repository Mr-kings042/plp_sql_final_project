# app/routers/books.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app import crud
from app.database import get_db

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=schemas.BookRead)
def create_book(book_in: schemas.BookCreate, db: Session = Depends(get_db)):
    try:
        book = crud.create_book(db, book_in)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return book

@router.get("/", response_model=list[schemas.BookRead])
def list_books(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return crud.list_books(db, skip, limit)

@router.get("/{book_id}", response_model=schemas.BookRead)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=schemas.BookRead)
def update_book(book_id: int, book_in: schemas.BookCreate, db: Session = Depends(get_db)):
    book = crud.update_book(db, book_id, book_in)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_book(db, book_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "deleted"}
