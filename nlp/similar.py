import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import nlp.cache as cache
import nlp.tools as tools
import own_tfidf
import own_tokenizer

BOOK_COLLECTION = {
    "11": "Alice's Adventures in Wonderland",
    "12": "Through the Looking-Glass",
    "16": "Peter Pan",
    "55": "The Wonderful Wizard of Oz",
    "113": "The Secret Garden",
    "120": "Treasure Island",
    "236": "The Jungle Book",
    "108": "The Return of Sherlock Holmes",
    "834": "The Memoirs of Sherlock Holmes",
    "863": "The Mysterious Affair at Styles",
    "1661": "The Adventures of Sherlock Holmes",
    "61262": "Poirot Investigates",
    "69087": "The murder of Roger Ackroyd",
    "70114": "The Big Four",
    "35": "The Time Machine",
    "36": "The War of the Worlds",
    "84": "Frankenstein; Or, The Modern Prometheus",
    "159": "The island of Doctor Moreau",
    "164": "Twenty Thousand Leagues under the Sea",
    "345": "Dracula",
    "68283": "The call of Cthulhu",
}


def get_collection_corpus():
    """Return book IDs and cleaned book texts from the collection."""
    corpus = []
    book_ids = []

    for book_id in BOOK_COLLECTION.keys():
        book_path = tools.get_path_file(book_id)

        if not os.path.exists(book_path):
            tools.download_book(book_id)

        book = tools.header_and_footer_remover(book_path)
        corpus.append(book)
        book_ids.append(book_id)

    return book_ids, corpus


def build_own_tfidf_matrix(corpus, language):
    """Build a TF-IDF matrix using the custom tokenizer."""
    corpus_tokens = []

    for book_text in corpus:
        tokenize = own_tokenizer.OwnTokenizer(data=book_text, lang=language)
        tokens = tokenize.tokenize(
            sentence=False, punct=True, stopword=True, lower=True
        )
        corpus_tokens.append(tokens)

    tfidf = own_tfidf.OwnTfidf()
    return tfidf.fit(corpus_tokens)


def build_sklearn_tfidf_matrix(corpus, language):
    """Build a TF-IDF matrix using scikit-learn."""
    vectorizer = TfidfVectorizer(stop_words=language, max_features=3000)
    return vectorizer.fit_transform(corpus)


def get_recommendation_titles(book_ids, similarity_scores, book_id, top):
    """Return the top recommended book titles."""
    sorted_indexes = similarity_scores.argsort()[::-1]
    recommendations = []

    for index in sorted_indexes:
        recommended_id = book_ids[index]
        if recommended_id == book_id:
            continue

        recommendations.append(BOOK_COLLECTION[recommended_id])

        if len(recommendations) == top:
            break

    return recommendations


def similar_books(book_id, top=5, own=False):
    """Return books similar to the requested book."""
    book_id = str(book_id)
    tag_name = "own" if own else None
    book_path = tools.get_path_file(book_id)

    cached = tools.setup_action(book_id, "similar", tag_name=tag_name)

    if cached is not None:
        return cached

    if book_id not in BOOK_COLLECTION:
        print(f"The book ID {book_id} is not in the collection.")
        return []

    book_ids, corpus = get_collection_corpus()
    language = tools.get_book_language(book_path)

    if own:
        tfidf_matrix = build_own_tfidf_matrix(corpus, language)
    else:
        tfidf_matrix = build_sklearn_tfidf_matrix(corpus, language)

    similarity_matrix = cosine_similarity(tfidf_matrix)
    target_index = book_ids.index(book_id)
    similarity_scores = similarity_matrix[target_index]

    recommendations = get_recommendation_titles(
        book_ids, similarity_scores, book_id, top
    )

    print(f"If you liked {BOOK_COLLECTION[book_id]}, you may also like: ")

    cache.save_cache(book_id, "similar", recommendations, tag_name=tag_name)

    return recommendations
