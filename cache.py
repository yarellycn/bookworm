import json
import os

CACHE_FOLDER = "data/cache"
BOOK_FOLDER = "data/books"
FILE_NAME_END = "_book.txt"


def book_in_cache(book_id):
    """Return True if the book is already stored locally."""
    book_filename = f"{book_id}{FILE_NAME_END}"
    book_path = os.path.join(BOOK_FOLDER, book_filename)
    return os.path.exists(book_path)


def get_cache_path(book_id, task, tag_name=None):
    """Return the cache file path for a book task."""
    if tag_name is not None:
        cache_filename = f"{book_id}_{task}_{tag_name}.json"
    else:
        cache_filename = f"{book_id}_{task}.json"

    return os.path.join(CACHE_FOLDER, cache_filename)


def charge_cache(book_id, task, tag_name=None):
    """Load cached data for a given book and task if available."""
    cache_path = get_cache_path(book_id, task, tag_name)

    try:
        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as file:
                return json.load(file)
        return None
    except Exception as e:
        print(f"Cache error. Unable to load cached data for book {book_id}: {e}")
        return None


def save_cache(book_id, task, data, tag_name=None):
    """Save task results to a JSON cache file."""
    if not os.path.isdir(CACHE_FOLDER):
        os.makedirs(CACHE_FOLDER)

    cache_path = get_cache_path(book_id, task, tag_name)

    try:
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Cache save failed for book {book_id} and task '{task}': {e}")
