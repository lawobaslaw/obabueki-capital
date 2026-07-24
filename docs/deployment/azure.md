# Azure Deployment

## Overview

The Obabueki Capital backend is deployed using Azure Container Apps.

The deployment follows cloud-native best practices by using Managed Identity instead of registry credentials.

---

## Azure Resources

| Resource                   | Name                            |
| -------------------------- | ------------------------------- |
| Resource Group             | rg-obabueki-capital-dev-uksouth |
| Azure Container Registry   | acrobabuekicapital              |
| Container Apps Environment | cae-obabueki-capital-dev        |
| Container App              | ca-obabueki-capital-api         |

---

## Deployment Architecture

```text
GitHub

    │

Docker Build

    │

Azure Container Registry

    ▲
Managed Identity
    ▲
Azure RBAC (AcrPull)

    │

Azure Container Apps

    │

FastAPI
```

---

## Deployment Process

1. Build Docker image
2. Push image to Azure Container Registry
3. Create Azure Container App
4. Assign Managed Identity
5. Grant AcrPull role
6. Configure registry authentication
7. Deploy application
8. Verify `/`, `/health` and `/docs`

---

## Lessons Learned

During deployment the following challenges were encountered:

- Azure Container Apps cannot pull from a private ACR until the Managed Identity has been granted the AcrPull role.
- Registry authentication should use Managed Identity rather than enabling the ACR admin account.
- Docker build context should be minimised using a correctly placed `.dockerignore`.
- Azure Container Apps ingress must match the application listening port (8000).

---

## Future Improvements

- Azure Database for PostgreSQL
- GitHub Actions Continuous Deployment
- Infrastructure as Code
- Azure Monitor
- Application Insights
