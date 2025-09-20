# Library Management System API

A comprehensive REST API for managing library operations built with FastAPI, SQLAlchemy, and MySQL. This system provides endpoints for managing books, authors, members, and loan transactions in a library setting.

## Features

- **Book Management**: Create, read, update, and delete books with support for multiple authors and categories
- **Author Management**: Manage author information and their associated works
- **Member Management**: Handle library member registration and information
- **Loan System**: Track book loans, returns, and availability
- **Database Integration**: MySQL database with proper relationships and constraints
- **API Documentation**: Auto-generated interactive API documentation with Swagger UI

## Tech Stack

- **Backend Framework**: FastAPI
- **Database**: MySQL 8.0+
- **ORM**: SQLAlchemy 1.4+
- **Data Validation**: Pydantic
- **Database Driver**: PyMySQL
- **Environment Management**: python-dotenv

## Project Structure

```
library-management-system/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database configuration and connection
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic schemas for request/response
│   ├── crud.py              # Database operations
│   ├── .env                 # Environment variables
│   ├── requirements.txt     # Python dependencies
│   └── routers/
│       ├── __init__.py
│       ├── books.py         # Book-related endpoints
│       ├── authors.py       # Author-related endpoints
│       ├── members.py       # Member-related endpoints
│       └── loans.py         # Loan-related endpoints
├── library.sql              # Database schema and initialization
└── README.md
```

## Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package installer)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Mr-kings042/plp_sql_final_project.git
cd plp_sql_final_project
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv menv

# Activate virtual environment
# On Windows:
menv\Scripts\activate
# On macOS/Linux:
source menv/bin/activate
```

### 3. Install Dependencies

```bash
cd app
pip install -r requirements.txt
```

### 4. Database Setup

#### Create MySQL Database

```bash
# Connect to MySQL
mysql -u root -p

# Run the schema file
source library.sql
```

Or execute the SQL file directly:
```bash
mysql -u root -p < library.sql
```

#### Configure Environment Variables

Create a `.env` file in the `app/` directory:

```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/library_db
```

Replace `username` and `password` with your MySQL credentials.

### 5. Run the Application

```bash
# From the app/ directory
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, access the interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Books
- `POST /api/v1/books/` - Create a new book
- `GET /api/v1/books/` - List all books (with pagination)
- `GET /api/v1/books/{book_id}` - Get a specific book
- `PUT /api/v1/books/{book_id}` - Update a book
- `DELETE /api/v1/books/{book_id}` - Delete a book

### Authors
- `POST /api/v1/authors/` - Create a new author
- `GET /api/v1/authors/` - List all authors (with pagination)

### Members
- `POST /api/v1/members/` - Register a new member
- `GET /api/v1/members/` - List all members (with pagination)
- `GET /api/v1/members/{member_id}` - Get a specific member

### Loans
- `POST /api/v1/loans/` - Create a new loan
- `POST /api/v1/loans/{loan_id}/return` - Return a borrowed book

## Usage Examples

### Create a Book

```bash
curl -X POST "http://localhost:8000/api/v1/books/" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "The Great Gatsby",
       "isbn": "978-0-7432-7356-5",
       "publication_year": 1925,
       "total_copies": 5,
       "available_copies": 5,
       "summary": "A classic American novel",
       "author_ids": [1],
       "category_ids": [1]
     }'
```

### Create a Loan

```bash
curl -X POST "http://localhost:8000/api/v1/loans/" \
     -H "Content-Type: application/json" \
     -d '{
       "book_id": 1,
       "member_id": 1,
       "loan_date": "2024-01-15",
       "due_date": "2024-02-15"
     }'
```

## Database Schema

The system uses the following main entities:

- **Books**: Core book information with ISBN, title, copies tracking
- **Authors**: Author details with many-to-many relationship to books
- **Categories**: Book categorization system
- **Members**: Library member information
- **Loans**: Loan transactions tracking borrowed books
- **Publishers**: Publisher information (optional relationship)

Key relationships:
- Books ↔ Authors (Many-to-Many)
- Books ↔ Categories (Many-to-Many)
- Books → Publisher (Many-to-One)
- Loans → Books (Many-to-One)
- Loans → Members (Many-to-One)

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Code Style

The project follows PEP 8 style guidelines. Use tools like `black` and `flake8` for code formatting:

```bash
pip install black flake8
black app/
flake8 app/
```

## Deployment

For production deployment:

1. **Environment Variables**: Set secure environment variables
2. **Database**: Use a production MySQL instance
3. **WSGI Server**: Use Gunicorn instead of Uvicorn for production
4. **Reverse Proxy**: Configure Nginx as a reverse proxy
5. **SSL**: Enable HTTPS with proper SSL certificates

Example production command:
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support or questions, please open an issue on the GitHub repository.