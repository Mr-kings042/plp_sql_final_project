# app/models.py
from sqlalchemy import Column, Integer, BigInteger, String, Text, ForeignKey, Date, Enum, Boolean, SmallInteger
from sqlalchemy.orm import relationship
from app.database import Base
import enum
from sqlalchemy.sql import func
from sqlalchemy import TIMESTAMP

class LoanStatus(enum.Enum):
    on_loan = "on_loan"
    returned = "returned"
    overdue = "overdue"

class Publisher(Base):
    __tablename__ = "publishers"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    address = Column(String(512))
    website = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())

    books = relationship("Book", back_populates="publisher")

class Author(Base):
    __tablename__ = "authors"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    bio = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    books = relationship("Book", secondary="book_authors", back_populates="authors")

class Category(Base):
    __tablename__ = "categories"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(512))

    books = relationship("Book", secondary="book_categories", back_populates="categories")

class Book(Base):
    __tablename__ = "books"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False)
    isbn = Column(String(20), nullable=False, unique=True)
    publisher_id = Column(BigInteger, ForeignKey("publishers.id"), nullable=True)
    publication_year = Column(SmallInteger)
    total_copies = Column(Integer, nullable=False, default=1)
    available_copies = Column(Integer, nullable=False, default=1)
    summary = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    publisher = relationship("Publisher", back_populates="books")
    authors = relationship("Author", secondary="book_authors", back_populates="books")
    categories = relationship("Category", secondary="book_categories", back_populates="books")
    loans = relationship("Loan", back_populates="book")

class BookAuthor(Base):
    __tablename__ = "book_authors"
    book_id = Column(BigInteger, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True)
    author_id = Column(BigInteger, ForeignKey("authors.id", ondelete="CASCADE"), primary_key=True)
    contribution = Column(String(100), default="author")

class BookCategory(Base):
    __tablename__ = "book_categories"
    book_id = Column(BigInteger, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True)
    category_id = Column(BigInteger, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True)

class Member(Base):
    __tablename__ = "members"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(50))
    address = Column(String(512))
    membership_date = Column(Date)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    loans = relationship("Loan", back_populates="member")

class Loan(Base):
    __tablename__ = "loans"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    book_id = Column(BigInteger, ForeignKey("books.id"), nullable=False)
    member_id = Column(BigInteger, ForeignKey("members.id"), nullable=False)
    loan_date = Column(Date)
    due_date = Column(Date)
    return_date = Column(Date, nullable=True)
    status = Column(Enum(LoanStatus), default=LoanStatus.on_loan)
    created_at = Column(TIMESTAMP, server_default=func.now())

    book = relationship("Book", back_populates="loans")
    member = relationship("Member", back_populates="loans")
