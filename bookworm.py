import argparse
from cache import book_in_cache
from tools import download_book
import topic_modeling as topic
import summarize
import similar
import lexical_diversity as lexdiv
import entities
import card

VALID_ACTIONS = {"lexdiv", "topics", "entities", "summarize", "similar", "card"}


def validate_book_id(book_id):
    if book_id <= 0:
        raise ValueError("Book id must be positive.")

    return book_id


def prepare_book(book_id):
    book_id = validate_book_id(book_id)

    if not book_in_cache(book_id):
        download_book(book_id)

    return book_id


def execute_action(action_type, book_id, own=False):
    """Function for notebook interface"""

    if action_type not in VALID_ACTIONS:
        raise ValueError(f"Unknown action: {action_type}")

    book_id = prepare_book(book_id)

    if action_type == "lexdiv":
        return lexdiv.get_lexical_diversity(book_id)

    elif action_type == "topics":
        return topic.topic(book_id, own=own)

    elif action_type == "entities":
        return entities.get_entities(book_id)

    elif action_type == "summarize":
        return summarize.summarize_book(book_id)

    elif action_type == "similar":
        return similar.similar_books(book_id, own=own)

    elif action_type == "card":
        return card.get_book_card(book_id)


def cli():
    parser = argparse.ArgumentParser(description="Etude de livre", allow_abbrev=False)

    groupe = parser.add_mutually_exclusive_group(required=True)
    groupe.add_argument("--lexdiv", type=int)
    groupe.add_argument("--topics", type=int)
    groupe.add_argument("--entities", type=int)
    groupe.add_argument("--summarize", type=int)
    groupe.add_argument("--similar", type=int)
    groupe.add_argument("--card", type=int)

    parser.add_argument("--own", action="store_true")

    args = parser.parse_args()

    if args.lexdiv:
        print(execute_action("lexdiv", args.lexdiv))
        return

    elif args.topics:
        print(execute_action("topics", args.topics, own=args.own))
        return

    elif args.entities:
        print(execute_action("entities", args.entities))
        return

    elif args.summarize:
        print(execute_action("summarize", args.summarize))
        return

    elif args.similar:
        print(execute_action("similar", args.similar, own=args.own))
        return

    elif args.card:
        print(execute_action("card", args.card))
        return


if __name__ == "__main__":
    try:
        cli()
    except ValueError as e:
        print(e)
