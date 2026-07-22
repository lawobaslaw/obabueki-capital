# Obabueki Capital

## Project Overview

Obabueki Capital is an investment portfolio management platform built with FastAPI.

The project follows a layered architecture.

```
API
↓

Service

↓

Repository

↓

SQLAlchemy Models

↓

PostgreSQL
```

---

# Tech Stack

- Python 3.14
- FastAPI
- SQLAlchemy 2.x
- Alembic
- PostgreSQL
- Pytest
- Ruff
- Black
- GitHub Actions
- Docker

---

# Coding Standards

- Follow PEP8.
- Use type hints everywhere.
- Use SQLAlchemy 2.0 style.
- Use Pydantic v2.
- Use Decimal for financial values.
- Use UUID primary keys.

---

# Architecture Rules

Business logic belongs in Services.

Repositories only access the database.

Routers remain thin.

Schemas validate input/output.

Models represent persistence.

---

# Testing

Every new feature must include tests.

Run before every commit:

python -m black .

python -m ruff check .

python -m pytest

---

# Branch Strategy

feature/*
↓

develop
↓

main

---

# Current Features

- Authentication
- Users
- Portfolios
- Accounts
- Transactions

---

# Next Feature

Holdings Engine

Transactions remain the single source of truth.

Holdings are calculated dynamically.

Do not create a holdings table.