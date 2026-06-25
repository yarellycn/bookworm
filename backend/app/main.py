from fastapi import FastAPI

from backend.app.api.books import router as books_router
from backend.app.api.health import router as health_router


app = FastAPI(title="Bookworm API")

app.include_router(books_router)
app.include_router(health_router)
