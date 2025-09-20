# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date


# Publishers
def list_publishers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Publisher).offset(skip).limit(limit).all()

def get_publisher(db: Session, publisher_id: int):
    return db.query(models.Publisher).filter(models.Publisher.id == publisher_id).first()
# Books
def create_book(db: Session, book_in: schemas.BookCreate):
    book = models.Book(
        title=book_in.title,
        isbn=book_in.isbn,
        publication_year=book_in.publication_year,
        total_copies=book_in.total_copies,
        available_copies=book_in.available_copies,
        summary=book_in.summary,
        publisher_id=book_in.publisher_id
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    # attach authors
    if book_in.author_ids:
        for aid in book_in.author_ids:
            author = db.get(models.Author, aid)
            if author:
                book.authors.append(author)
    if book_in.category_ids:
        for cid in book_in.category_ids:
            cat = db.get(models.Category, cid)
            if cat:
                book.categories.append(cat)
    db.commit()
    db.refresh(book)
    return book

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def list_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def update_book(db: Session, book_id: int, book_in: schemas.BookCreate):
    book = get_book(db, book_id)
    if not book:
        return None
    book.title = book_in.title
    book.isbn = book_in.isbn
    book.publication_year = book_in.publication_year
    book.total_copies = book_in.total_copies
    book.available_copies = book_in.available_copies
    book.summary = book_in.summary
    book.publisher_id = book_in.publisher_id
    # update relations (simple replace)
    if book_in.author_ids is not None:
        book.authors = []
        for aid in book_in.author_ids:
            author = db.get(models.Author, aid)
            if author:
                book.authors.append(author)
    if book_in.category_ids is not None:
        book.categories = []
        for cid in book_in.category_ids:
            cat = db.get(models.Category, cid)
            if cat:
                book.categories.append(cat)
    db.commit()
    db.refresh(book)
    return book

def delete_book(db: Session, book_id: int):
    book = get_book(db, book_id)
    if not book:
        return False
    db.delete(book)
    db.commit()
    return True

# Authors
def create_author(db: Session, author_in: schemas.AuthorCreate):
    author = models.Author(**author_in.dict())
    db.add(author)
    db.commit()
    db.refresh(author)
    return author

def list_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()

# Members
def create_member(db: Session, member_in: schemas.MemberCreate):
    member = models.Member(**member_in.dict())
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

def get_member(db: Session, member_id: int):
    return db.query(models.Member).filter(models.Member.id == member_id).first()

def list_members(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Member).offset(skip).limit(limit).all()

# Loans
def create_loan(db: Session, loan_in: schemas.LoanCreate):
    # ensure book available
    book = db.get(models.Book, loan_in.book_id)
    member = db.get(models.Member, loan_in.member_id)
    if not book:
        raise ValueError("Book not found")
    if not member:
        raise ValueError("Member not found")
    if book.available_copies < 1:
        raise ValueError("No copies available")
    loan = models.Loan(
        book_id=loan_in.book_id,
        member_id=loan_in.member_id,
        loan_date=loan_in.loan_date,
        due_date=loan_in.due_date,
        status=models.LoanStatus.on_loan
    )
    book.available_copies -= 1
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan

def return_loan(db: Session, loan_id: int):
    loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    if not loan:
        return None
    if loan.status == models.LoanStatus.returned:
        return loan
    loan.return_date = date.today()
    loan.status = models.LoanStatus.returned
    # increment book available copies
    book = loan.book
    if book:
        book.available_copies = (book.available_copies or 0) + 1
    db.commit()
    db.refresh(loan)
    return loan
