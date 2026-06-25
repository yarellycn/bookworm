from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.books import router as books_router
from backend.app.api.health import router as health_router


app = FastAPI(title="Bookworm API")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  #Only these URLs are allowed
    allow_credentials=True,  #Allows cookies/auth headers
    allow_methods=["*"],  #Allows all HTTP methods from the frontend
    allow_headers=["*"],  #Allows the frontend to send headers
)

app.include_router(books_router)
app.include_router(health_router)
