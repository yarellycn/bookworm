import os
import urllib.request
import xml.etree.ElementTree as ET

import cache
import entities
import lexical_diversity as lexdiv
import similar
import summarize
import tools
import topic_modeling as topic

RDF_FOLDER = "data/rdf"
RDF_FILE_END = "_book.rdf"
GUTENBERG_RDF_URL = "https://www.gutenberg.org/cache/epub/"


def download_metadata_rdf(book_id):
    """Download the RDF metadata file and save it locally."""
    rdf_url = f"{GUTENBERG_RDF_URL}{book_id}/pg{book_id}.rdf"
    rdf_filename = get_rdf_filename(book_id)

    # Si le folder "rdf" n'existe pas, le créer.
    if not os.path.isdir(RDF_FOLDER):
        os.makedirs(RDF_FOLDER)

    rdf_path = get_rdf_path(book_id)

    try:
        # Télécharger le rdf et le sauvegarder localement.
        urllib.request.urlretrieve(rdf_url, rdf_path)
        print(f"File {rdf_filename} successfully downloaded.")
    except Exception as e:
        print(f"Unable to download RDF for book {book_id}: {e}")


def get_rdf_filename(book_id):
    """Return the RDF filename associated with a book ID."""
    return f"{book_id}{RDF_FILE_END}"


def get_rdf_path(book_id):
    """Return the local path of a RDF file."""
    rdf_file_name = get_rdf_filename(book_id)
    return os.path.join(RDF_FOLDER, rdf_file_name)


def parse_metadata_rdf(rdf_path):
    """Parse an RDF metadata file and return selected book metadata."""
    parsed_rdf = ET.parse(rdf_path)
    root = parsed_rdf.getroot()

    namespaces = {
        "pgterms": "http://www.gutenberg.org/2009/pgterms/",
        "dcterms": "http://purl.org/dc/terms/",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    }

    title = root.find(".//dcterms:title", namespaces)

    authors = []
    for creator in root.findall(".//dcterms:creator//pgterms:name", namespaces):
        authors.append(creator.text)

    authors = ", ".join(authors)

    bookshelves = []
    for shelf in root.findall(".//pgterms:bookshelf//rdf:value", namespaces):
        shelf_name = shelf.text.replace("Category: ", "")
        bookshelves.append(shelf_name)

    bookshelves = ", ".join(bookshelves)

    return {
        "title": title.text if title is not None else "",
        "authors": authors,
        "bookshelves": bookshelves,
    }


def book_info(book_id):
    """Return the basic metadata for a book."""
    rdf_path = get_rdf_path(book_id)

    if not os.path.exists(rdf_path):
        download_metadata_rdf(book_id)

    if not os.path.exists(rdf_path):
        return None

    metadata = parse_metadata_rdf(rdf_path)

    result = {
        "id": str(book_id),
        "title": metadata["title"],
        "authors": metadata["authors"],
        "bookshelves": metadata["bookshelves"],
    }

    return result


def get_book_card(book_id, action="card"):
    """Return the card information for a book."""
    cached = tools.setup_action(book_id, action)

    if cached is not None:
        return cached

    result = {
        "info": book_info(book_id),
        "lexdiv": lexdiv.get_lexical_diversity(book_id),
        "topics": topic.topic(book_id),
        "entities": entities.get_entities(book_id),
        "summary": summarize.summarize_book(book_id),
        "similar": similar.similar_books(book_id),
    }

    cache.save_cache(book_id, action, result)
    return result
