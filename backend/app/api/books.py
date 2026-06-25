from fastapi import APIRouter, HTTPException

from nlp.card import get_book_card

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/{book_id}/card")
def book_card(book_id: int):
    if book_id <= 0:
        raise HTTPException(status_code=400, detail="Book id must be positive.")

    card = get_book_card(book_id)

    if card is None:
        raise HTTPException(status_code=404, detail="Book not found.")

    return card
