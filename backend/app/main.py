from fastapi import FastAPI
from fastapi.routing import APIRoute

from app.api.auth import router as auth_router

app = FastAPI(
    title="Obabueki Capital API",
    version="0.1.0",
)

app.include_router(auth_router)
for route in auth_router.routes:
    print(route.path, route.methods)


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


for route in app.routes:
    if isinstance(route, APIRoute):
        print(route.path, route.methods)
