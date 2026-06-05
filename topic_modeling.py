import re, tools, cache
from sklearn.feature_extraction.text import TfidfVectorizer
import own_Tokenizer as own_Tok

def section_cuter(book_id):
    """ Cut each Chapter and return it in tuple"""
    path_book = tools.get_path_file(tools.get_book_file(book_id))
    book = tools.header_and_footer_remover(path_book)
    # Split avec regex pour chapter et ignore des type maj,min assemblé.
    section_brut = re.split(r'CHAPTER\s+[IVXLCDM\d]+|Chapter\s+\d+', book, flags=re.IGNORECASE)
    #supression du sommaire
    section_brut= section_brut[1:]
    # Mise en place du len pour suprimer les mini decoupe du sommaire 
    sections = [s.strip() for s in section_brut if len(s.strip()) > 100]
    return sections

def topic (book_id, action = "topics"):
    path_book = tools.get_path_file(tools.get_book_file(book_id))

    cached = tools.setup_action(book_id, action)

    if cached is not None:
        return cached

    sections= section_cuter(book_id)
    lang = tools.get_book_language(path_book).lower()

    super_tok = own_Tok.OwnTokenizer(data=cached, lang= lang)
 
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
    return dictionnaire_final




