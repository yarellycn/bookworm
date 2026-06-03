import string, re, urllib.request ,os
from nltk import word_tokenize
import tools, cache

url= "https://www.gutenberg.org/ebooks/"
url_end=".txt.utf-8"


def download_book(book_id):
   try :
    url_final = f"{url}{book_id}{url_end}"
    name_file = f"{book_id}_book.txt"
    book_folder = "Data/Books"
    path_file= os.path.join(book_folder,name_file)
    urllib.request.urlretrieve(url_final,path_file)
    print(f"Fichier {name_file} correctement téléchargé")
    return path_file
   except:
      print(f"Erreur lors du telechargement de {book_id}")

def read_text_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()
    
def header_and_footer_remover(path_file):
    """Clean the start and end balise of Gutenberg projet"""
    data = read_text_file(path_file)

    start_match = re.search(r"\*\*\*\s*START OF THE PROJECT GUTENBERG EBOOK.*?\*\*\*", data, flags=re.IGNORECASE)
    end_match = re.search(r"\*\*\*\s*END OF THE PROJECT GUTENBERG EBOOK.*?\*\*\*", data, flags=re.IGNORECASE)
    if start_match and end_match:
        index_debut = start_match.end() 
        index_fin = end_match.start() 
        texte = data[index_debut:index_fin]
        # print (texte)
        return texte.strip()
    
    print(f" Balises de début/fin non détectées dans {path_file} !")
    return data.strip()


def get_book_language(path_file):
    try:
        with open(path_file, "r", encoding="utf-8") as file:
            data = file.read()
        # on prend les donné avant la balise start
        start_match = re.search(r"\*\*\*\s*START OF THE PROJECT GUTENBERG EBOOK.*?\*\*\*", data, flags=re.IGNORECASE)
        
        if start_match:
            en_tete = data[:start_match.start()]
        else:
            en_tete = data
        match = re.search(r"Language:\s+([a-zA-Z-]+)", en_tete, flags=re.IGNORECASE)
        
        if match:
            return match.group(1).strip().lower()
        
        return "english"
        
    except ValueError as e:
        print("Impossible de lire la langue dans {path_file}: {e}")
        return 
    
def cleaner(file_path):
    text = header_and_footer_remover(file_path)
    tokens = word_tokenize(text)
    return [word.lower() for word in tokens if word not in string.punctuation]

def setup_action(book_id, action):
   
   cache_action = cache.charge_cache(book_id, action)
   
   if cache_action is not None:
        return cache_action
   
   if not cache.book_in_cache(book_id):
        
        tools.download_book(book_id)
   
def get_tokens(book_id):
    book_file = f"{book_id}_book.txt"
    path_file = os.path.join("Data/Books", book_file)
    
    cleaned_tokens = cleaner(path_file)
    return cleaned_tokens
