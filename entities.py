import spacy

import cache
import tools
from nltk import ne_chunk, pos_tag, word_tokenize

nlp = spacy.load("en_core_web_sm")

def clean_entity(name):
    name = name.replace("\n", " ").strip()
    name = name.replace("'s", "").replace("’s", "")
    name = name.removeprefix("the ")
    name = name.removeprefix("The ")
    return " ".join(name.split())


def is_valid_entity(name):
    bad_words = {
        "chapter", "fig", "extras", "un_important",
        "said", "down", "latitude", "longitude"
    }

    if len(name) < 2:
        return False

    if name.lower() in bad_words:
        return False

    if name.lower().startswith("chapter"):
        return False

    return True

def get_entities(book_id, action="entities"):
    cached = tools.setup_action(book_id, action)

    if cached is not None:
        return cached

    # Tokenize the book into sentences.
    sentences = tools.get_sentences(book_id)
    characters = set()
    locations = set()

    for sentence in sentences:
        tokens = word_tokenize(sentence)
        tagged_words = pos_tag(tokens)
        chunked_sentences = ne_chunk(tagged_words)

        for chunk in chunked_sentences:
            if hasattr(chunk, "label"):
                name = " ".join(word for word, _ in chunk)

                if chunk.label() == "PERSON":
                    characters.add(name)

                elif chunk.label() in ["GPE", "LOCATION"]:
                    locations.add(name)

    result = {
        "characters": (sorted(characters)),
        "locations": (sorted(locations))
    }

    cache.save_cache(book_id, action, result)
    return result

def get_entities_(book_id, action="entitiesdd"):
    cached = tools.setup_action(book_id, action)

    if cached is not None:
        return cached
    
    book_file = tools.get_book_file(book_id)
    path_file = tools.get_path_file(book_file)
    text = tools.header_and_footer_remover(path_file)

    doc = nlp(text)

    characters = set()
    locations = set()

    for entity in doc.ents:
        name = clean_entity(entity.text)

        if not is_valid_entity(name):
            continue

        if entity.label_ == "PERSON":
            characters.add(name)

        elif entity.label_ in ["GPE", "LOC", "FAC"]:
            locations.add(name)

    result = {
        "characters": (sorted(characters)),
        "locations": (sorted(locations))
    }

    cache.save_cache(book_id, action, result)
    return result
