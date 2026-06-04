import tools, cache, os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BOOK_COLLECTION = {"11": "Alice's Adventures in Wonderland",
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
    "345": "Dracula", "68283": "The call of Cthulhu"
}

def similar_books(id_ask, top=5):

    cached = tools.setup_action(id_ask,"similar")

    if cached is not None:
        return cached

    if id_ask not in BOOK_COLLECTION:
        print(" L'id livre n'est pas dan la collection")
        return []

    corpus = []
    book_ids = []
    for book_id in BOOK_COLLECTION.keys():
        path_book = f"Data/Books/{book_id}_book.txt"
        
        if not os.path.exists(path_book):
            tools.download_book(book_id)
        
        book = tools.header_and_footer_remover(path_book)
        lang = tools.get_book_language(path_book)
        corpus.append(book)
        book_ids.append(book_id)

    
    vectorizer = TfidfVectorizer(stop_words=lang,max_features=3000)
    tfidf_matrix = vectorizer.fit_transform(corpus)

    matrix_similar = cosine_similarity(tfidf_matrix)

    target_index = book_ids.index(id_ask)

    score = matrix_similar[target_index]
    index_sort= score.argsort()[::-1]

    reco_list = []
    for id in index_sort:
        reco_id = book_ids[id]
        if reco_id == id_ask:
            continue
        
        reco_list.append(BOOK_COLLECTION[reco_id])

        if len(reco_list)== top:
            break
    
    print(f" Si vous avez lu {BOOK_COLLECTION[id_ask]} , vous devriez aimer : ")
    print(reco_list)
    cache.save_cache(id_ask,"similar", reco_list)
    return reco_list
        





    
    