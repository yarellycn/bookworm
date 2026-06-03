import os, json

FOLDER_CACHE = "Data/Cache"


def book_in_cache(book_id):
    name_file = f"{book_id}_book.txt"
    if os.path.exists(f"{FOLDER_CACHE}/{name_file}"):
        return True
    return False

def charge_cache(book_id, task):
    """Fonction de chargement de du cache si existant"""

    folder_file = os.path.join(FOLDER_CACHE, f"{book_id}_{task}.json")

    try:
        if os.path.exists(folder_file):
            with open(folder_file, "r", encoding="utf-8") as file:
                return json.load(file)
        return None
    except:
        print(f"Erreur chache , Impossible de recherche le livre {book_id} en cache")


def save_cache(book_id, task, data):
    """Creation du cache avec ID et fonction utilisé , cache en json"""

    if not os.path.exists(FOLDER_CACHE):
        os.makedirs(FOLDER_CACHE)

    try:
        folder_file = os.path.join(FOLDER_CACHE, f"{id_book}_{task}.json")
        with open(folder_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except:
        print(
            "Sauvegare du cache impossible pour le livre : {id_book} avec le fonction : {task}"
        )
