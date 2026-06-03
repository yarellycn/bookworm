import string, re
from urllib.request import urlopen

def download_book(book_id):
    """Downloads the text of the book with the given ID and saves it."""
    # f stands for format string, which allows us to insert variables into the string.
    url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"

    # Connect to the URL
    response = urlopen(url)

    # Read the content of the response
    text = response.read().decode("utf-8")

    filename = f"{book_id}_book.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)

    return filename

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