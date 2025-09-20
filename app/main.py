from fastapi import FastAPI
from app.database import engine, Base
from app.routers import books, authors, members, loans,publishers
from app import seed

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Library Management System", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    """Run startup tasks"""
    seed.create_sample_publishers()

app.include_router(books.router, prefix="/api/v1")
app.include_router(authors.router, prefix="/api/v1")
app.include_router(members.router, prefix="/api/v1")
app.include_router(loans.router, prefix="/api/v1")
app.include_router(publishers.router, prefix="/api/v1")

@app.get("/")
async def read_root():
    return {"Hello": "There!",
            "message": "Welcome to the Library Management System API"}
