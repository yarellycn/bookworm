import argparse
import topic_modeling as topic
import summarize
import similar
import lexical_diversity as lexdiv
import entities
import card

# main_file = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# if main_file not in sys.path:
#     sys.path.append(main_file)


def run_bookworm(action_type, book_id, own=False):
    """ Function for notebook interface """

    if action_type == "lexdiv":
        return lexdiv.get_lexical_diversity(book_id)

    elif action_type == "topics":
        return topic.topic(book_id)

    elif action_type == "entities":
        return entities.get_entities(book_id)

    elif action_type == "summarize":
        return summarize.summarize_book(book_id)

    elif action_type == "similar":
        return similar.similar_books(book_id, ownCooking=own)

    elif action_type == "card":
        return card.get_book_card(book_id)

def cli():
    parser = argparse.ArgumentParser(description="Etude de livre")

    groupe = parser.add_mutually_exclusive_group(required=True)
    groupe.add_argument("--lexdiv", type=int)
    groupe.add_argument("--topics", type=int)
    groupe.add_argument("--entities", type=int)
    groupe.add_argument("--summarize",type=int)
    groupe.add_argument("--similar", type=int)
    groupe.add_argument("--card", type=int)

    parser.add_argument("--own",action="store_true")
    parser.add_argument("ask", type=str, nargs="*")

    args = parser.parse_args()

    if args.lexdiv:
        print(lexdiv.get_lexical_diversity(args.lexdiv))
        return

    elif args.topics:
        print(topic.topic(args.topics, own=args.own))
        return

    elif args.entities:
        print(entities.get_entities(args.entities))
        return

    elif args.summarize:
        print(summarize.summarize_book(args.summarize))
        return

    elif args.similar:
        print(similar.similar_books(args.similar, ownCooking=args.own))
        return

    elif args.card:
        print(card.get_book_card(args.card))
        return

if __name__ == "__main__":
    cli()

# if book_id is None:
#     raise ValueError("Please specify a book id.")

# if (book_id <= 0) or not isinstance(book_id, int):
#     raise ValueError("book_id incorrect.")