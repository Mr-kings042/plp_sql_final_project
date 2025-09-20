# app/routers/members.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app import crud
from app.database import get_db

router = APIRouter(prefix="/members", tags=["members"])

@router.post("/", response_model=schemas.MemberRead)
def create_member(member_in: schemas.MemberCreate, db: Session = Depends(get_db)):
    return crud.create_member(db, member_in)

@router.get("/", response_model=list[schemas.MemberRead])
def list_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_members(db, skip, limit)

@router.get("/{member_id}", response_model=schemas.MemberRead)
def get_member(member_id: int, db: Session = Depends(get_db)):
    member = crud.get_member(db, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member
