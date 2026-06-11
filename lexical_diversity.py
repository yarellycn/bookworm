from nltk import FreqDist

import cache
import tools


def frequency_count(tokens):
    """Return the frequency count of each word in the book."""
    return FreqDist(tokens)


def number_of_tokens_occurring_once(tokens):
    """Return the number of word tokens that appear only once."""
    frequency = frequency_count(tokens)
    tokens_occurring_once = [word for word, count in frequency.items() if count == 1]
    return len(tokens_occurring_once)


def average_word_length(tokens):
    """Return the average word length."""
    if not tokens:
        return 0

    return sum(len(word) for word in tokens) / len(tokens)


def get_lexical_diversity(book_id, action="lexdiv"):
    """Return lexical diversity metrics for a book."""
    cached = tools.setup_action(book_id, action)

    if cached is not None:
        return cached

    tokens = tools.get_tokens(book_id)

    total_tokens = len(tokens)
    unique_tokens = len(set(tokens))
    hapax = number_of_tokens_occurring_once(tokens)

    result = {
        "tok": total_tokens,
        "typ": unique_tokens,
        "hap": hapax,
        "ttr": unique_tokens / total_tokens if total_tokens else 0,
        "mwl": average_word_length(tokens),
        "mwf": total_tokens / unique_tokens if unique_tokens else 0,
    }

    cache.save_cache(book_id, action, result)
    return result
