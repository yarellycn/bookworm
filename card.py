import os

import urllib.request
import xml.etree.ElementTree as ET

import cache
import lexical_diversity as lexdiv
import topic_modeling as topic
import entities
import summarize
import similar
import tools


def get_metadata_rdf(book_id):
    rdf_url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.rdf"

    rdf_folder = "data/rdf"
    rdf_file_name = f"{book_id}_book.rdf"
    rdf_path= os.path.join(rdf_folder,rdf_file_name)

    if os.path.exists(rdf_path):
        return rdf_path
    
    try:
        urllib.request.urlretrieve(rdf_url,rdf_path)
        return rdf_path
    except Exception as e:
        print(f"Unable to download RDF for book {book_id}: {e}")
        return None

def parse_metadata_rdf(rdf_path):
    parsed_rdf = ET.parse(rdf_path)
    root = parsed_rdf.getroot()

    namespaces = {
        "pgterms": "http://www.gutenberg.org/2009/pgterms/",
        "dcterms": "http://purl.org/dc/terms/",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
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
        "title": title.text,
        "authors": authors,
        "bookshelves": bookshelves
    }

def book_info(book_id):
    rdf_path = get_metadata_rdf(book_id)

    if rdf_path is None:
        return None
    
    metadata = parse_metadata_rdf(rdf_path)

    result = {
        "id": f"{book_id}",
        "authors": metadata["authors"],
        "bookshelves": metadata["bookshelves"]
    }

    return result

def get_book_card(book_id, action="card"):
    cached = tools.setup_action(book_id, action)

    if cached is not None:
        return cached

    result = {
        "info": book_info(book_id),
        "lexdiv": lexdiv.get_lexical_diversity(book_id,),
        "topics": topic.topic(book_id),
        "entities": entities.get_entities(book_id),
        "summary": summarize.summarize_book(book_id),
        "similar": similar.similar_books(book_id)
    }

    cache.save_cache(book_id, action, result)
    return result