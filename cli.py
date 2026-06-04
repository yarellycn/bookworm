import argparse, sys, os
import topic_modeling as topic
import lexical_diversity as lexdiv
import entities

main_file = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if main_file not in sys.path:
    sys.path.append(main_file)

import tools


def cli():

    parser = argparse.ArgumentParser(description="Etude de livre")

    groupe = parser.add_mutually_exclusive_group(required=True)
    groupe.add_argument("--lexdiv", type=int)
    groupe.add_argument("--topics", action="store_true")
    groupe.add_argument("--entities", type=int)
    groupe.add_argument("--summarize", action="store_true")
    groupe.add_argument("--similar", action="store_true")
    groupe.add_argument("--card", action="store_true")

    parser.add_argument("ask", type=str, nargs="*")

    args = parser.parse_args()


    if args.lexdiv:
        print(lexdiv.get_lexical_diversity(args.lexdiv))
        return

    elif args.topics:
        topic.topic(args.ask[0])
        return

    elif args.entities:
        print(entities.get_entities(args.entities))
        return

    elif args.summarize:
        return

    elif args.similar:
        return

    elif args.card:
        return
    

if __name__ == "__main__":
    cli()

# if book_id is None:
#     raise ValueError("Please specify a book id.")

# if (book_id <= 0) or not isinstance(book_id, int):
#     raise ValueError("book_id incorrect.")