import argparse
from typing import IO
import sys
from src.main.db_helpers import get_from_db, parse_db_data, get_comics


def main(args, out: IO[str] = sys.stdout) -> None:
    """
    Cli application to get comics.
    Provides list of availbe comics with -l option
    Provides link to the comics with -n <num> option where num is the number id of the comics.
    Provides link to the comics with -t <title> option where title is the title of the comics.

    Parameters
    ----------
    args : argparse.Namespace()
        Argument passed to cli.
    out : IO[str]
        Handle to write to

    Returns
    -------
    None    
    """

    #create an argparser
    parser = argparse.ArgumentParser(add_help=False)
    #create a group to create mutually excusive arguments
    group = parser.add_mutually_exclusive_group()

    #add arguments
    parser.add_argument(
        '-h',
        '--help',
        action='help',
        default=argparse.SUPPRESS,
        help='use -h to get the help on how to use this application')
    group.add_argument('-n',
                       '--number',
                       type=int,
                       help="get the comics with the number id NUMBER")
    group.add_argument('-t',
                       '--title',
                       help="get the comics with the title TITLE")
    group.add_argument('-l',
                       '--list',
                       action='store_true',
                       help="list of available comics")

    #parse arguments
    args = parser.parse_args()

    #invoke the right function according to arguments
    if args.list:
        try:
            out.write("get comics from db\n")
            data = get_from_db(81)
            out.write("parse comics\n")
            parse_db_data(data)
            exit(0)
        except Exception as e:
            out.write(f"{e}")
            exit(1)

    elif args.number:
        try:
            url = get_comics(n=args.number)
            out.write(f"{url}")
            exit(0)
        except Exception as e:
            out.write(f"{e}")
            exit(1)

    elif args.title:
        try:
            url = get_comics(t=args.title)
            out.write(f"{url}")
            exit(0)
        except Exception as e:
            out.write(f"{e}")
            exit(1)


if __name__ == "__main__":

    main(sys.argv[1:])
