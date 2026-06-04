import cache
import tools

from nltk import FreqDist


def number_of_word_tokens(tokens):
    """Return the number of word tokens in the book."""
    return len(tokens)

def frequency_count(tokens):
    """Return the frequency count of each word in the book."""
    frequency_count = FreqDist(word for word in tokens)
    return frequency_count

def number_of_unique_word_tokens(tokens):
    """Return the number of unique words in the book."""
    return len(set(tokens))

def number_of_tokens_occurring_once(tokens):
    frequency = frequency_count(tokens)
    tokens_occurring_once = [word for word, count in frequency.items() if count == 1]
    return len(tokens_occurring_once)

def ratio_of_unique_word_tokens_to_word_tokens(tokens):
    ratio = number_of_unique_word_tokens(tokens) / number_of_word_tokens(tokens)
    return ratio

def average_word_length(tokens):
    return sum(len(word) for word in tokens) / len(tokens)

def ratio_of_word_tokens_to_unique_word_tokens(tokens):
    ratio = number_of_word_tokens(tokens) / number_of_unique_word_tokens(tokens)
    return ratio

def get_lexical_diversity(book_id, action="lexdiv"):
    """Return the lexical diversity of a book."""
    cached = tools.setup_action(book_id, action)

    if cached is not None:
        return cached

    tokens = tools.get_tokens(book_id)

    result = {
        "tok": int(number_of_word_tokens(tokens)),
        "typ": int(number_of_unique_word_tokens(tokens)),
        "hap": int(number_of_tokens_occurring_once(tokens)),
        "ttr": float(ratio_of_unique_word_tokens_to_word_tokens(tokens)),
        "mwl": float(average_word_length(tokens)),
        "mwf": float(ratio_of_word_tokens_to_unique_word_tokens(tokens))
    }

    cache.save_cache(book_id, action, result)
    return result