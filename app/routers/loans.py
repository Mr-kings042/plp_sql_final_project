# app/routers/loans.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app import crud
from app.database import get_db

router = APIRouter(prefix="/loans", tags=["loans"])

@router.post("/", response_model=schemas.LoanRead)
def create_loan(loan_in: schemas.LoanCreate, db: Session = Depends(get_db)):
    try:
        loan = crud.create_loan(db, loan_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return loan

@router.post("/{loan_id}/return", response_model=schemas.LoanRead)
def return_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = crud.return_loan(db, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan
