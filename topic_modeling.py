import re, tools, cache
from sklearn.feature_extraction.text import TfidfVectorizer

def section_cuter(book_id):
    path_book = f"Data/Books/{book_id}_book.txt"
    book = tools.header_and_footer_remover(path_book)
    section_brut = re.split(r'CHAPTER\s+[IVXLCDM\d]+|Chapter\s+\d+', book, flags=re.IGNORECASE)
    sections = [s.strip() for s in section_brut if len(s.strip()) > 100]
    return sections

def topic (book_id, action = "topics"):
    path_book = f"Data/Books/{book_id}_book.txt"

    cached = tools.setup_action(book_id, action)

    if cached is not None:
        return cached

    sections= section_cuter(book_id)
    lang = tools.get_book_language(path_book).lower()
    vectorizer = TfidfVectorizer(
        # tokenizer=tools.get_token, 
        # lowercase=False, 
        stop_words=lang,
        max_features=3000
    )
    
    tfidf_matrix = vectorizer.fit_transform(sections)
    
    # enregistre de la position des mot dans la matrice 
    noms_des_mots = vectorizer.get_feature_names_out()
    
    dictionnaire_final = {}

    for index_section, ligne_matrix in enumerate(tfidf_matrix):
        scores_mots = ligne_matrix.toarray()[0]
        #classement par index du plus faible au plus fort scrore de la matrice
        index_tries = scores_mots.argsort()
        #investion obligatoire pour avoir les dix meilleur 
        top_10_index = index_tries[-10:][::-1]
        
        top_10_mots = [noms_des_mots[i] for i in top_10_index if scores_mots[i] > 0]
        dictionnaire_final[str(index_section + 1)] = top_10_mots

    cache.save_cache(book_id, action, dictionnaire_final)
    print(dictionnaire_final)
    return dictionnaire_final




