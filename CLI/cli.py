import argparse, sys, os

main_file = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if main_file not in sys.path:
    sys.path.append(main_file)

from Cache import cache


def cli():

    parser = argparse.ArgumentParser(description="Etude de livre")

    groupe = parser.add_mutually_exclusive_group(required=True)
    groupe.add_argument("--lexdiv", action="store_true")
    groupe.add_argument("--topics", action="store_true")
    groupe.add_argument("--entities", action="store_true")
    groupe.add_argument("--summarize", action="store_true")
    groupe.add_argument("--similar", action="store_true")
    groupe.add_argument("--card", action="store_true")

    parser.add_argument("ask", type=str, nargs="*")

    args = parser.parse_args()

    if args.lexdiv is not None:
        return

    elif args.topics is not None:
        return

    elif args.entities is not None:
        return

    elif args.summarize is not None:
        return

    elif args.similar is not None:
        return

    elif args.card is not None:
        return
