from collections import Counter

from nltk import ne_chunk, pos_tag, word_tokenize

import cache
import tools


PERSON_CLUES = {
    "mr",
    "mrs",
    "miss",
    "ms",
    "sir",
    "lady",
    "lord",
    "king",
    "queen",
    "captain",
    "doctor",
    "dr",
    "professor",
    "father",
    "mother",
}

LOCATION_CLUES = {
    "in",
    "at",
    "from",
    "to",
    "near",
    "inside",
    "outside",
    "toward",
    "towards",
    "through",
    "across",
    "around",
    "into",
}


def clean_entity(name):
    """Clean spacing and possessive forms from an entity name."""
    name = name.replace("'s", "").replace("’s", "")
    name = name.removeprefix("the ")
    name = name.removeprefix("The ")
    name = name.strip("_")
    return " ".join(name.split())


def is_valid_entity(name):
    """Return True if an entity name should be kept."""
    if len(name) < 2:
        return False

    if name.lower().startswith("chapter"):
        return False

    if name.endswith(" THE"):
        return False

    if name.lower() in {"english", "french"}:
        return False

    if name.isupper():
        return False

    return True


def looks_like_sentence_start_false_positive(name, sentence):
    """Return True if the entity is likely to be a sentence-start false positive."""
    words = word_tokenize(sentence)

    if not words:
        return False

    first_word = clean_entity(words[0])

    return name == first_word and len(name.split()) == 1


def has_person_context(name, sentence):
    """Return True if the entity appears in a person-related context."""
    lowered = sentence.lower()
    name_lower = name.lower()

    for clue in PERSON_CLUES:
        if f"{clue} {name_lower}" in lowered:
            return True

    return False


def has_location_context(name, sentence):
    """Return True if the entity appears in a location-related context."""
    lowered = sentence.lower()
    name_lower = name.lower()

    for clue in LOCATION_CLUES:
        if f"{clue} {name_lower}" in lowered:
            return True

    return False


def get_entities(book_id, action="entities"):
    """Extract characters and locations using NLTK"""
    cached = tools.setup_action(book_id, action)

    if cached is not None:
        return cached

    # Tokenize the book into sentences.
    sentences = tools.get_sentences(book_id)

    # Compteurs pour les personnages, lieux et faux positifs.
    character_counts = Counter()
    location_counts = Counter()
    sentence_start_counts = Counter()

    # Compteurs pour les indices de contexte.
    character_context = Counter()
    location_context = Counter()

    for sentence in sentences:
        # Appliquer le pipeline NLTK : tokenisation, POS tagging et NER.
        tokens = word_tokenize(sentence)
        tagged_words = pos_tag(tokens)
        chunked_sentences = ne_chunk(tagged_words)

        for chunk in chunked_sentences:
            # Ignorer les éléments qui ne sont pas des entités nommées.
            if not hasattr(chunk, "label"):
                continue

            # Reconstruire et nettoyer le nom de l'entité.
            name = " ".join(word for word, _ in chunk)
            name = clean_entity(name)

            # Ignorer les entités jugées invalides.
            if not is_valid_entity(name):
                continue

            # Détecter les entités apparaissant uniquement en début de phrase.
            if looks_like_sentence_start_false_positive(name, sentence):
                sentence_start_counts[name] += 1

            # Compter les personnages et leurs indices de contexte.
            if chunk.label() == "PERSON":
                character_counts[name] += 1

                if has_person_context(name, sentence):
                    character_context[name] += 1

            # Compter les lieux et leurs indices de contexte.
            elif chunk.label() in ["GPE", "LOCATION"]:
                location_counts[name] += 1

                if has_location_context(name, sentence):
                    location_context[name] += 1

    characters = {
        name
        for name, count in character_counts.items()
        if (count >= 3 or character_context[name] >= 1)
        and not (len(name.split()) == 1 and sentence_start_counts[name] >= count)
    }

    locations = {
        name
        for name, count in location_counts.items()
        if (count >= 3 or location_context[name] >= 1)
        and not (len(name.split()) == 1 and sentence_start_counts[name] >= count * 0.6)
    }

    result = {"characters": sorted(characters), "locations": sorted(locations)}

    cache.save_cache(book_id, action, result)
    return result
