import re, tools

def section_cuter(book_id):
    path_book = f"Data/Books/{book_id}_book.txt"
    book = tools.read_text_file(path_book)
    section_brut = re.split(r'CHAPTER\s+[IVXLCDM\d]+|Chapter\s+\d+', book, flags=re.IGNORECASE)
    sections = [s.strip() for s in section_brut if len(s.strip()) > 100]
    return sections

def topic (book_id):
    
    return




