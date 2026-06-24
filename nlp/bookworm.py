import argparse

import nlp.card as card
import nlp.entities as entities
import nlp.lexical_diversity as lexdiv
import nlp.similar as similar
import nlp.summarize as summarize
import nlp.topic_modeling as topic
from nlp.cache import book_in_cache
from nlp.tools import download_book

VALID_ACTIONS = {"lexdiv", "topics", "entities", "summarize", "similar", "card"}


def validate_book_id(book_id):
    """Validate and return a positive book ID."""
    if book_id <= 0:
        raise ValueError("Book id must be positive.")

    return book_id


def prepare_book(book_id):
    """Validate the book ID and download the book if needed."""
    book_id = validate_book_id(book_id)

    if not book_in_cache(book_id):
        download_book(book_id)

    return book_id


def execute_action(action_type, book_id, own=False):
    """Execute the selected action."""

    if action_type not in VALID_ACTIONS:
        raise ValueError(f"Unknown action: {action_type}")

    book_id = prepare_book(book_id)

    if action_type == "lexdiv":
        return lexdiv.get_lexical_diversity(book_id)

    if action_type == "topics":
        return topic.topic(book_id, own=own)

    if action_type == "entities":
        return entities.get_entities(book_id)

    if action_type == "summarize":
        return summarize.summarize_book(book_id)

    if action_type == "similar":
        return similar.similar_books(book_id, own=own)

    if action_type == "card":
        return card.get_book_card(book_id)


def cli():
    """Run the command-line interface."""
    parser = argparse.ArgumentParser(description="Etude de livre", allow_abbrev=False)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--lexdiv", type=int)
    group.add_argument("--topics", type=int)
    group.add_argument("--entities", type=int)
    group.add_argument("--summarize", type=int)
    group.add_argument("--similar", type=int)
    group.add_argument("--card", type=int)

    parser.add_argument("--own", action="store_true")

    args = parser.parse_args()

    if args.lexdiv:
        print(execute_action("lexdiv", args.lexdiv))
        return

    if args.topics:
        print(execute_action("topics", args.topics, own=args.own))
        return

    if args.entities:
        print(execute_action("entities", args.entities))
        return

    if args.summarize:
        print(execute_action("summarize", args.summarize))
        return

    if args.similar:
        print(execute_action("similar", args.similar, own=args.own))
        return

    if args.card:
        print(execute_action("card", args.card))
        return


if __name__ == "__main__":
    try:
        cli()
    except ValueError as e:
        print(e)
    except ConnectionError as e:
        print(f"Error : {e} ")
