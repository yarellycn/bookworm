import string, re, urllib.request ,os
import cache, tools

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
    
def true_text(path_file):
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
    
def cleaner(tokens):
    return [word.lower() for word in tokens if word not in string.punctuation]

def setup_action(book_id, action):
   
   cache_action = cache.charge_cache(book_id, action)
   
   if cache_action is not None:
        return cache_action
   
   if not cache.book_in_cache(book_id):
        tools.download_book(book_id)
   