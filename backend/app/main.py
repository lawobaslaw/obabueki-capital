from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.portfolio import router as portfolio_router
from app.api.account import router as account_router
from app.api.transaction import router as transaction_router
from app.api.holding import router as holding_router
from app.api.valuation import router as valuation_router

app = FastAPI(
    title="Obabueki Capital API",
    version="0.1.0",
)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(portfolio_router)
app.include_router(account_router)
app.include_router(transaction_router)
app.include_router(holding_router)
app.include_router(valuation_router)


@app.get("/")
def root():
    return {
        "application": "Obabueki Capital",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }
