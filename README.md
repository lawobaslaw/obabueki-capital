# Obabueki Capital

[![CI Status](https://github.com/lawobaslaw/obabueki-capital/actions/workflows/backend-ci.yml/badge.svg)](https://github.com/lawobaslaw/obabueki-capital/actions/workflows/backend-ci.yml)

> A cloud-native portfolio management platform built with FastAPI, Microsoft Azure and modern DevOps practices.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub_Actions-success)
![Azure](https://img.shields.io/badge/Azure-Container_Apps-0078D4)
![Azure](https://img.shields.io/badge/ACR-Private_Registry-0078D4)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active_Development-orange)

---

## Overview

Obabueki Capital is a backend-first portfolio management platform built as a long-term software engineering project to develop production-grade Backend, Cloud and DevOps skills while solving a real investment tracking problem.

The project is developed incrementally using:

- Test-Driven Development (TDD)
- Layered Architecture
- Docker
- GitHub Actions
- Microsoft Azure

while documenting engineering decisions through Architecture Decision Records (ADRs).

The application serves two purposes:

1. Build a production-quality investment portfolio management platform.
2. Demonstrate modern Backend, Cloud and DevOps engineering practices.

---

## Live Demo

The backend API is currently deployed to Microsoft Azure Container Apps.

- API: <https://ca-obabueki-capital-api.salmonmoss-e10d18e7.uksouth.azurecontainerapps.io>
- Swagger UI: <https://ca-obabueki-capital-api.salmonmoss-e10d18e7.uksouth.azurecontainerapps.io/docs>
- Health Check: <https://ca-obabueki-capital-api.salmonmoss-e10d18e7.uksouth.azurecontainerapps.io/health>

---

## Why I Built This

I wanted a single application capable of tracking investments across multiple platforms including:

- Trading 212
- Binance
- Nigerian Exchange (NGX)
- Future brokerage accounts

Rather than building another demo application, I chose to build software that solves a real problem while serving as a long-term Backend, Cloud and DevOps portfolio.

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

| Capability               | Status |
| ------------------------ | :----: |
| Docker                   |   ✅   |
| Docker Compose           |   ✅   |
| GitHub Actions CI        |   ✅   |
| Ruff                     |   ✅   |
| Black                    |   ✅   |
| Pytest                   |   ✅   |
| Azure Container Registry |   ✅   |
| Azure Container Apps     |   ✅   |
| Managed Identity         |   ✅   |
| Azure RBAC               |   ✅   |
| Azure Deployment         |   ✅   |
| Continuous Deployment    |   🚧   |
| Infrastructure as Code   |   🚧   |
| Monitoring               |   🚧   |
| Logging                  |   🚧   |

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

Each layer has a single responsibility, making the application easier to understand, test and maintain.

---

## Cloud Architecture

```text
                    GitHub

                       │

              GitHub Actions (CI)

                       │

                Docker Image

                       │

                       ▼

       Azure Container Registry

                       │

                       ▼

       Azure Container Apps

                       │

                       ▼

          FastAPI Backend API

                       │

                       ▼

     Azure PostgreSQL (planned)
```

---

## Technology Stack

## Backend

- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL (planned)
- Pydantic

## Testing

- Pytest
- Mocking
- Test-Driven Development (TDD)

## Code Quality

- Ruff
- Black

## DevOps Cloud

- Docker
- Docker Compose
- GitHub Actions
- Azure Container Registry
- Azure Container Apps

## Cloud

- Microsoft Azure

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

Development follows a documented engineering process.

For the project's vision, engineering principles, roadmap and Definition of Done, see:

```test
docs/PROJECT_CHARTER.md
```

---

## Running Locally

Clone the repository.

```bash
git clone https://github.com/lawobaslaw/obabueki-capital.git

cd obabueki-capital
```

## Docker

```bash
docker compose up --build
```

## Local Development

```bash
python -m venv .venv

pip install -r backend/requirements.txt

uvicorn app.main:app --reload
```

---

## Running Tests

```bash
pytest

ruff check .

black --check .
```

---

## Azure Deployment

The backend is currently deployed to Microsoft Azure using:

- Azure Container Registry (ACR)
- Azure Container Apps
- Managed Identity
- Azure RBAC (AcrPull)

API documentation is available through the deployed application:

```test
https://<container-app-url>/docs
```

Deployment documentation:

```text
docs/azure-deployment.md
```

---

## Repository Structure

```text
backend/
frontend/
docs/
infrastructure/
.github/
docker-compose.yml
README.md
```

---

## Roadmap

### ✅ v0.8.0-alpha — First Cloud Deployment

- Azure Container Registry
- Azure Container Apps
- Managed Identity
- Azure RBAC
- Public HTTPS deployment

---

### 🚧 v0.9.0-beta — Production Readiness

- Azure PostgreSQL
- Environment Variables
- Alembic Migrations
- GitHub Actions Continuous Deployment
- Monitoring
- Logging

---

### 🔮 v1.0.0

- Portfolio Performance
- Asset Allocation
- Dividend Tracking
- Dashboard
- CSV Import
- Live Market Data
- AI-powered Portfolio Insights
- Infrastructure as Code

---

## Learning Journey

This repository documents my journey towards becoming a Backend, Cloud and DevOps Engineer.

Every feature is developed incrementally, tested thoroughly and reviewed before moving to the next milestone.

The objective is not simply to build software, but to demonstrate professional engineering practices from development through deployment and operations.

---

## License

This project is licensed under the MIT License.
