from fastapi import FastAPI, HTTPException
from nlp.card import get_book_card

app = FastAPI(title="Bookworm API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/books/{book_id}/card")
def book_card(book_id: int):
    if book_id <= 0:
        raise HTTPException(status_code=400, detail="Book id must be positive.")

    card = get_book_card(book_id)

    if card is None:
        raise HTTPException(status_code=400, detail="Book not found.")

    return card
