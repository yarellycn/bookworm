from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.text_rank import TextRankSummarizer

import cache
import tools


def summarize_book(book_id, sentence_count=4):
    """Generate and return a summary of a book using TextRank."""
    cached = tools.setup_action(book_id, action="summarize")

    if cached is not None:
        return cached

    book_path = tools.get_path_file(book_id)
    language = tools.get_book_language(book_path)
    text = tools.header_and_footer_remover(book_path)

    parser = PlaintextParser.from_string(text, Tokenizer(language))
    summarizer = TextRankSummarizer()

    best_sentences = summarizer(parser.document, sentence_count)

    summary_sentences = [str(sentence) for sentence in best_sentences]
    ordered_sentences = sorted(summary_sentences, key=lambda sentence: text.find(sentence))

    summary_string = " ".join(ordered_sentences)

    cache.save_cache(book_id, task="summarize", data=summary_string)

    return summary_string
