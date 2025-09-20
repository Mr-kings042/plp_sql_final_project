# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date

# Publisher
class PublisherBase(BaseModel):
    name: str
    address: Optional[str] = None
    website: Optional[str] = None

class PublisherCreate(PublisherBase):
    pass

class PublisherRead(PublisherBase):
    id: int
    class Config:
        orm_mode = True


# Author
class AuthorBase(BaseModel):
    first_name: str
    last_name: str
    bio: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class AuthorRead(AuthorBase):
    id: int
    class Config:
        orm_mode = True

# Category
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int
    class Config:
        orm_mode = True

# Book
class BookBase(BaseModel):
    title: str
    isbn: str
    publication_year: Optional[int] = None
    total_copies: int = 1
    available_copies: int = 1
    summary: Optional[str] = None

class BookCreate(BookBase):
    author_ids: Optional[List[int]] = []
    category_ids: Optional[List[int]] = []
    publisher_id: Optional[int] = None

class BookRead(BookBase):
    id: int
    authors: List[AuthorRead] = []
    categories: List[CategoryRead] = []
    publisher: Optional[PublisherRead] = None
    class Config:
        orm_mode = True

# Member
class MemberBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None

class MemberCreate(MemberBase):
    pass

class MemberRead(MemberBase):
    id: int
    class Config:
        orm_mode = True

# Loan
class LoanBase(BaseModel):
    book_id: int
    member_id: int
    loan_date: date
    due_date: date

class LoanCreate(LoanBase):
    pass

class LoanRead(LoanBase):
    id: int
    status: str
    return_date: Optional[date] = None
    class Config:
        orm_mode = True
