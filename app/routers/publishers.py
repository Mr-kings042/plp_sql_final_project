# app/routers/publishers.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app import crud
from app.database import get_db

router = APIRouter(prefix="/publishers", tags=["publishers"])

@router.get("/", response_model=list[schemas.PublisherRead])
def list_publishers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all publishers with pagination"""
    return crud.list_publishers(db, skip, limit)

@router.get("/{publisher_id}", response_model=schemas.PublisherRead)
def get_publisher(publisher_id: int, db: Session = Depends(get_db)):
    """Get a specific publisher by ID"""
    publisher = crud.get_publisher(db, publisher_id)
    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")
    return publisher