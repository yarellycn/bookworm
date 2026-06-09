import os
import re
import string
import urllib.error
import urllib.request

from nltk import sent_tokenize, word_tokenize

import cache

GUTENBERG_URL = "https://www.gutenberg.org/ebooks/"
GUTENBERG_URL_END = ".txt.utf-8"

BOOK_FOLDER = "data/books"
FILE_NAME_END = "_book.txt"

START_PATTERN = r"\*\*\*\s*START OF THE PROJECT GUTENBERG EBOOK.*?\*\*\*"
END_PATTERN = r"\*\*\*\s*END OF THE PROJECT GUTENBERG EBOOK.*?\*\*\*"


def download_book(book_id):
    """Download a book from Project Gutenberg and save it locally."""
    url_final = f"{GUTENBERG_URL}{book_id}{GUTENBERG_URL_END}"
    name_file = get_book_file(book_id)

    # Si le folder "books" n'existe pas, le créer.
    if not os.path.isdir(BOOK_FOLDER):
        os.makedirs(BOOK_FOLDER)

    path_file = get_path_file(book_id)

    try:
        # Télécharger le livre et le sauvegarder localement.
        urllib.request.urlretrieve(url_final, path_file)
        print(f"File {name_file} successfully downloaded.")

    except urllib.error.HTTPError:
        # Signaler un ID de livre invalide (due to 404 server response)
        raise ValueError(
            f"This book id ({book_id}) does not exist. Try again with another number."
        )

    except urllib.error.URLError:
        # Signaler un problème de connection.
        raise ConnectionError("Network is unreachable. Check your internet connection.")


def read_text_file(filename):
    """Return the contents of a text file as a string."""
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def get_gutenberg_markers(data):
    """Return the start and end Gutenberg markers found in the text."""
    start_match = re.search(START_PATTERN, data, flags=re.IGNORECASE)
    end_match = re.search(END_PATTERN, data, flags=re.IGNORECASE)

    return start_match, end_match


def header_and_footer_remover(path_file):
    """Remove the Project Gutenberg header and footer from a book."""
    data = read_text_file(path_file)

    # Rechercher les marqueurs de début et de fin ajoutés par Gutenberg.
    start_match, end_match = get_gutenberg_markers(data)

    if start_match and end_match:
        start_index = start_match.end()
        end_index = end_match.start()
        text = data[start_index:end_index]
        return text.strip()

    print(f"Start/end markers not found in {path_file}!")
    return data.strip()


def get_book_language(path_file):
    """Extract and return the book language from the Gutenberg metadata."""
    data = read_text_file(path_file)

    try:
        # Rechercher le marqueur de début ajouté par Gutenberg.
        start_match, _ = get_gutenberg_markers(data)

        if start_match:
            header = data[: start_match.start()]
        else:
            header = data

        match = re.search(r"Language:\s+([a-zA-Z-]+)", header, flags=re.IGNORECASE)

        if match:
            return match.group(1).strip().lower()

        return "english"

    except Exception as e:
        print(f"Impossible de lire la langue dans {path_file}: {e}")
        return None


def clean_and_word_tokenize(file_path):
    """Tokenize the text and remove punctuation."""
    text = header_and_footer_remover(file_path)
    tokens = word_tokenize(text)
    return [word.lower() for word in tokens if word not in string.punctuation]


def setup_action(book_id, action, tag_name=None):
    """Load cached data or download the book if needed."""
    cache_action = cache.charge_cache(book_id, action, tag_name=tag_name)

    if cache_action is not None:
        return cache_action

    # Télécharger le livre uniquement s'il n'est pas encore disponible localement.
    if not cache.book_in_cache(book_id):
        download_book(book_id)


def get_book_file(book_id):
    """Return the filename associated with a book ID."""
    return f"{book_id}{FILE_NAME_END}"


def get_path_file(book_id):
    """Return the local path of a downloaded book."""
    book_file = get_book_file(book_id)
    return os.path.join(BOOK_FOLDER, book_file)


def get_tokens(book_id):
    """Return the cleaned tokens of a book."""
    path_file = get_path_file(book_id)

    cleaned_tokens = clean_and_word_tokenize(path_file)
    return cleaned_tokens


def get_sentences(book_id):
    """Return the tokenized sentences of a book."""
    path_file = get_path_file(book_id)
    book_content_cleaned = header_and_footer_remover(path_file)
    sentences = sent_tokenize(book_content_cleaned)

    return sentences
