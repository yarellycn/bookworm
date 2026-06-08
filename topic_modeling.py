import re
import tools
import cache
from sklearn.feature_extraction.text import TfidfVectorizer
import own_Tokenizer as own_Tok
import own_tfidf
import numpy as np


def regex_cut(book):
    part_cut = re.split(r"PART\s+[IVXLCDM\d]+|Part\s+\d+", book, flags=re.IGNORECASE)
    if len(part_cut) > 1:
        return part_cut
    else:
        return re.split(
            r"CHAPTER\s+[IVXLCDM\d]+|Chapter\s+\d+", book, flags=re.IGNORECASE
        )


def section_cuter(book_id):
    """Cut each Chapter and return it in tuple"""
    path_book = tools.get_path_file(book_id)
    book = tools.header_and_footer_remover(path_book)
    # Split avec regex pour chapter et ignore des type maj,min assemblé.
    section_brut = regex_cut(book=book)
    # supression du sommaire
    section_brut = section_brut[1:]
    # Mise en place du len pour suprimer les mini decoupe du sommaire
    sections = [s.strip() for s in section_brut if len(s.strip()) > 100]
    return sections


def topic(book_id, action="topics", own=False):
    path_book = tools.get_path_file(book_id)
    if own:
        cached = tools.setup_action(book_id, action, tagName="own")
    else:
        cached = tools.setup_action(book_id, action)

    if cached is not None:
        return cached

    sections = section_cuter(book_id)
    lang = tools.get_book_language(path_book).lower()

    if own:
        corpus = []
        for chapter in sections:
            tok = own_Tok.OwnTokenizer(data=chapter, lang=lang)
            token_clean = tok.tokenize(lower=True, stopword=True, punct=True)
            corpus.append(token_clean)
        vectorizerOwn = own_tfidf.OwnTfidf()
        tfidf_matrix = vectorizerOwn.fit(corpus=corpus)
        word_name = vectorizerOwn.get_feature_name_out()
        print(word_name)

    else:
        vectorizer = TfidfVectorizer(
            # tokenizer=tools.get_token,
            # lowercase=False,
            stop_words=lang,
            max_features=3000,
        )
        tfidf_matrix = vectorizer.fit_transform(sections)

        # enregistre de la position des mot dans la matrice
        word_name = vectorizer.get_feature_names_out()

    dictionnaire_final = {}

    for index_section, ligne_matrix in enumerate(tfidf_matrix):
        # Sk learn à ça propre matrice sans les 0 , obligé de faire avec une condition pour passer le argsort
        if own:
            words_scores = np.array(ligne_matrix)
        else:
            words_scores = ligne_matrix.toarray()[
                0
            ]  # [0] a cause du tableau de tableau

        # classement par index du plus faible au plus fort scrore de la matrice
        index_tries = words_scores.argsort()
        # print(index_tries)

        # investion obligatoire pour avoir les dix meilleur
        top_10_index = index_tries[-10:][::-1]

        top_10_words = [word_name[i] for i in top_10_index if words_scores[i] > 0]
        dictionnaire_final[str(index_section + 1)] = top_10_words
    if own:
        cache.save_cache(book_id, action, dictionnaire_final, tagName="own")
    else:
        cache.save_cache(book_id, action, dictionnaire_final)
    return dictionnaire_final
