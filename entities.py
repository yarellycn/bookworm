import spacy

import cache
import tools
from collections import Counter
from nltk import ne_chunk, pos_tag, word_tokenize

nlp = spacy.load("en_core_web_sm")

PERSON_CLUES = {
    "mr", "mrs", "miss", "ms", "sir", "lady", "lord", "king", "queen",
    "captain", "doctor", "dr", "professor", "father", "mother"
}

LOCATION_CLUES = {
    "in", "at", "from", "to", "near", "inside", "outside", "toward",
    "towards", "through", "across", "around", "into"
}

def clean_entity(name):
    name = name.replace("'s", "").replace("’s", "")
    name = name.removeprefix("the ")
    name = name.strip("_")
    name = name.removeprefix("The ")
    return " ".join(name.split())

def is_valid_entity(name):
    if len(name) < 2:
        return False

    if name.lower().startswith("chapter"):
        return False
    
    if name.endswith(" THE"):
        return False
    
    if name.startswith("_"):
        return False
    
    if name.lower() in {"english", "french"}:
        return False
    
    if name.isupper():
        return False

    return True

def looks_like_sentence_start_false_positive(name, sentence):
    words = word_tokenize(sentence)

    if not words:
        return False

    first_word = clean_entity(words[0])

    return name == first_word and len(name.split()) == 1

def has_person_context(name, sentence):
    lowered = sentence.lower()
    name_lower = name.lower()

    for clue in PERSON_CLUES:
        if f"{clue} {name_lower}" in lowered:
            return True

    return False

def has_location_context(name, sentence):
    lowered = sentence.lower()
    name_lower = name.lower()

    for clue in LOCATION_CLUES:
        if f"{clue} {name_lower}" in lowered:
            return True

    return False

def get_entities_spacy(book_id, action="spacy"):
    cached = tools.setup_action(book_id, action)

    if cached is not None:
        return cached
    
    path_file = tools.get_path_file(book_id)
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

def get_entities(book_id, action="entities"):
    cached = tools.setup_action(book_id, action)

    if cached is not None:
        return cached

    # Tokenize the book into sentences.
    sentences = tools.get_sentences(book_id)

    character_counts = Counter()
    location_counts = Counter()
    sentence_start_counts = Counter()

    character_context = Counter()
    location_context = Counter()

    for sentence in sentences:
        tokens = word_tokenize(sentence)
        tagged_words = pos_tag(tokens)
        chunked_sentences = ne_chunk(tagged_words)

        for chunk in chunked_sentences:
            if not hasattr(chunk, "label"):
                continue

            name = " ".join(word for word, _ in chunk)
            name = clean_entity(name)

            if not is_valid_entity(name):
                continue

            if looks_like_sentence_start_false_positive(name, sentence):
                sentence_start_counts[name] += 1

            if chunk.label() == "PERSON":
                character_counts[name] += 1

                if has_person_context(name, sentence):
                    character_context[name] += 1

            elif chunk.label() in ["GPE", "LOCATION"]:
                location_counts[name] += 1

                if has_location_context(name, sentence):
                    location_context[name] += 1

    characters = {
        name for name, count in character_counts.items()
        if (
            count >= 3
            or character_context[name] >= 1
            or len(name.split()) >= 2 and count >= 2
            )
        and not (
            len(name.split()) == 1
            and sentence_start_counts[name] >= count
    )
    }

    locations = {
        name for name, count in location_counts.items()
        if (
            count >= 3
            or location_context[name] >= 1
            or len(name.split()) >= 2
        )
        and not (
            len(name.split()) == 1
            and sentence_start_counts[name] >= count * 0.6
        )
    }

    result = {
        "characters": sorted(characters),
        "locations": sorted(locations)
    }

    cache.save_cache(book_id, action, result)
    return result