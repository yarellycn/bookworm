import re

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

import cache
import own_tfidf
import own_tokenizer as own_tok
import tools


def regex_cut(book):
    """Split a book by parts or chapters."""
    sections = re.split(r"PART\s+[IVXLCDM\d]+|Part\s+\d+", book, flags=re.IGNORECASE)

    if len(sections) > 1:
        return sections

    return re.split(r"CHAPTER\s+[IVXLCDM\d]+|Chapter\s+\d+", book, flags=re.IGNORECASE)


def section_cutter(book_id):
    """Split a book by chapters or parts."""
    book_path = tools.get_path_file(book_id)
    book = tools.header_and_footer_remover(book_path)
    # Split avec regex pour chapter et ignorer des type maj, min assemblés.
    raw_sections = regex_cut(book=book)
    # Supprimer les petites sections issues du sommaire.
    raw_sections = raw_sections[1:]
    # Mise en place du len pour suprimer les mini decoupes du sommaire
    sections = [s.strip() for s in raw_sections if len(s.strip()) > 100]
    return sections


def build_own_tfidf_matrix(sections, language):
    """Build a TF-IDF matrix using the custom tokenizer."""
    corpus = []

    for section in sections:
        tokenizer = own_tok.OwnTokenizer(data=section, language=language)
        tokens = tokenizer.tokenize(lower=True, stopword=True, punct=True)
        corpus.append(tokens)

    own_vectorizer = own_tfidf.OwnTfidf()
    tfidf_matrix = own_vectorizer.fit(corpus=corpus)
    feature_names = own_vectorizer.get_feature_name_out()

    return tfidf_matrix, feature_names


def build_sklearn_tfidf_matrix(sections, language):
    """Build a TF-IDF matrix using scikit-learn."""
    vectorizer = TfidfVectorizer(
        # tokenizer=tools.get_token,
        # lowercase=False,
        stop_words=language,
        max_features=3000,
    )
    tfidf_matrix = vectorizer.fit_transform(sections)

    # Enregistrement de la position des mots dans la matrice.
    feature_names = vectorizer.get_feature_names_out()

    return tfidf_matrix, feature_names


def get_top_words_by_section(tfidf_matrix, feature_names, own=False):
    """Return the top TF-IDF words for each section."""
    result = {}

    for index_section, matrix_row in enumerate(tfidf_matrix):
        # Sk learn a sa propre matrice sans les 0, obligé de faire avec une condition pour passer le argsort.
        if own:
            words_scores = np.array(matrix_row)
        else:
            words_scores = matrix_row.toarray()[0]  # [0] a cause du tableau de tableau

        # Classement par index du plus faible au plus fort score de la matrice.
        sorted_indexes = words_scores.argsort()

        # Inversion obligatoire pour avoir les dix meilleurs.
        top_10_indexes = sorted_indexes[-10:][::-1]

        top_10_words = [feature_names[i] for i in top_10_indexes if words_scores[i] > 0]

        result[str(index_section + 1)] = top_10_words

    return result


def topic(book_id, action="topics", own=False):
    """Return the top topic words for each book section."""
    tag_name = "own" if own else None
    cached = tools.setup_action(book_id, action, tag_name=tag_name)

    if cached is not None:
        return cached

    book_path = tools.get_path_file(book_id)
    language = tools.get_book_language(book_path).lower()
    sections = section_cutter(book_id)

    if own:
        tfidf_matrix, feature_names = build_own_tfidf_matrix(sections, language)
    else:
        tfidf_matrix, feature_names = build_sklearn_tfidf_matrix(sections, language)

    result = get_top_words_by_section(tfidf_matrix, feature_names, own=own)

    cache.save_cache(book_id, action, result, tag_name=tag_name)

    return result
