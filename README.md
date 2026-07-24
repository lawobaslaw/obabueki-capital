# Obabueki Capital

[![CI Status](https://github.com/lawobaslaw/obabueki-capital/actions/workflows/backend-ci.yml/badge.svg)](https://github.com/lawobaslaw/obabueki-capital/actions/workflows/backend-ci.yml)

> A modern portfolio management platform built with FastAPI and modern DevOps practices.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub_Actions-success)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active_Development-orange)

---

## Overview

Obabueki Capital is a portfolio management platform built as a long-term engineering project to develop production-grade Backend, Cloud and DevOps skills while solving a real investment tracking problem.

The project is being developed incrementally using **Test-Driven Development (TDD)**, **Layered Architecture**, **Docker**, **GitHub Actions**, and **Azure** while documenting engineering decisions through Architecture Decision Records (ADRs).

The application serves two purposes:

1. Build a production-quality portfolio management platform.
2. Demonstrate modern Backend, Cloud and DevOps engineering practices.

---

## Why I Built This

I wanted a single application capable of tracking investments across multiple platforms including:

- Trading 212
- Binance
- Nigerian Exchange (NGX)
- Future brokerage accounts

Rather than building a demo project, I chose to build software that solves a real problem while serving as a long-term DevOps and Cloud Engineering portfolio.

---

## Current Project Status

## Product

| Feature                | Status |
| ---------------------- | :----: |
| Authentication         |   ✅   |
| Portfolio Management   |   ✅   |
| Account Management     |   ✅   |
| Transaction Management |   ✅   |
| Holdings Engine        |   ✅   |
| Price Service          |   ✅   |
| Account Valuation      |   ✅   |
| Portfolio Summary      |   ✅   |
| Portfolio Performance  |   🚧   |
| Dashboard              |   🚧   |

---

## DevOps

| Capability             | Status |
| ---------------------- | :----: |
| Docker                 |   ✅   |
| Docker Compose         |   ✅   |
| GitHub Actions CI      |   ✅   |
| Ruff                   |   ✅   |
| Black                  |   ✅   |
| Pytest                 |   ✅   |
| Azure Deployment       |   🚧   |
| Infrastructure as Code |   🚧   |
| Monitoring             |   🚧   |
| Logging                |   🚧   |
| Continuous Deployment  |   🚧   |

---

## Architecture

The backend follows a layered architecture.

```text
API
 │
 ▼
Services
 │
 ▼
Calculations
 │
 ▼
Repositories
 │
 ▼
Database
```

Each layer has a single responsibility, making the application easier to test and maintain.

---

## Technology Stack

### Backend

- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Pydantic

### Testing

- Pytest
- Mocking
- Test-Driven Development (TDD)

### Code Quality

- Ruff
- Black

### DevOps (used)

- Docker
- Docker Compose
- GitHub Actions

### Cloud (Current Focus)

- Azure Container Registry
- Azure Container Apps
- Azure PostgreSQL
- GitHub Actions CD
- Infrastructure as Code (planned)

---

## Engineering Principles

This project follows:

- Test-Driven Development (TDD)
- Single Responsibility Principle (SRP)
- Dependency Injection
- Layered Architecture
- Incremental Delivery
- CI before CD
- Architecture Decision Records (ADRs)

---

## Engineering Process

This project is developed using a documented engineering process.

For the project's vision, engineering principles, roadmap, and definition of done, see:

📄 **docs/PROJECT_CHARTER.md**

---

## Running Locally

```bash
git clone https://github.com/lawobaslaw/obabueki-capital.git

cd obabueki-capital

docker compose up --build
```

---

## Running Tests

```bash
pytest

ruff check .

black --check .
```

---

## Roadmap

### ✅ v0.7.0

- Portfolio valuation
- Portfolio summary
- Price service
- Improved testing

### 🚧 v0.8.0 (Current Milestone)

Cloud Ready

- Azure deployment
- GitHub Actions CD
- Azure Container Registry
- Infrastructure as Code
- Monitoring
- Logging

### 🔮 Future

- Portfolio performance
- Dashboard
- Dividend tracking
- CSV import
- Live market data
- Reporting
- AI-powered portfolio insights

---

## Repository Structure

```text
backend/
frontend/
docs/
.github/
docker-compose.yml
README.md
```

---

## Learning Journey

This repository documents my transition towards becoming a DevOps / Cloud Engineer.

Every feature is developed incrementally, tested thoroughly, and reviewed before moving on to the next milestone.

The goal is not simply to build software, but to demonstrate professional engineering practices from development through deployment.

---

## License

This project is licensed under the MIT License.
