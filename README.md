# Backend API

A FastAPI-based backend with user authentication and PostgreSQL integration.

## Features

- FastAPI framework with async support
- PostgreSQL database with SQLAlchemy ORM
- User authentication with JWT
- Docker and docker-compose setup
- Modular project structure

## Setup

1. Clone the repository
```bash
git clone [your-repo-url]
cd [repo-name]
```

2. Create .env file (use .env.example as template)
```bash
cp .env.example .env
# Edit .env with your configurations
```

3. Run with Docker
```bash
docker-compose up --build
```

The API will be available at:
- Backend API: http://localhost:8000
- PostgreSQL: localhost:5432

## Project Structure

```
.
├── database/           # Database configuration and session management
├── models/            # SQLAlchemy models and Pydantic schemas
├── routers/           # API routes
├── services/         # Business logic
├── main.py          # FastAPI application
├── requirements.txt  # Python dependencies
└── docker-compose.yml
```
