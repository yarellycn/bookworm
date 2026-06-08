import tools
import cache
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer


def summarize_book(book_id, sentence_count=4):
    cached = tools.setup_action(book_id, action="summarize")

    if cached is not None:
        return cached

    path_book = tools.get_path_file(book_id)
    lang = tools.get_book_language(path_book)
    text = tools.header_and_footer_remover(path_book)

    parser = PlaintextParser.from_string(text, Tokenizer(lang))
    summarizer = TextRankSummarizer()

    best_sentences = summarizer(parser.document, sentence_count)
    sentence_string = [str(s) for s in best_sentences]
    chrono_sentences = sorted(sentence_string, key=lambda s: text.find(s))
    summary_string = " ".join(chrono_sentences)
    cache.save_cache(book_id, task="summarize", data=summary_string)
    return summary_string
