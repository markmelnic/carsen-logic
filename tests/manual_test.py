import os, sys, inspect
from argparse import ArgumentParser, RawTextHelpFormatter

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from db import DB
from mobile_de.methods import search, surface_search, checker
from settings import TEST_SEARCH_PARAMS
import scalg, csv

if __name__ == "__main__":
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        "test_nr",
        metavar="test number",
        type=int,
        help="Which test would you like to run.",
    )
    args = parser.parse_args()

    # test search and print output
    if args.test_nr == 2:
        dataset = search(TEST_SEARCH_PARAMS, db=False)
        for dt in dataset:
            print(dt[1:])
    # run a surface search and print output
    elif args.test_nr == 3:
        dataset = surface_search(TEST_SEARCH_PARAMS)
        for dt in dataset:
            print(dt[1:])
    # test database creation
    elif args.test_nr == 4:
        db = DB()
        db.close_conn()
    # test database creation and add values from test search
    elif args.test_nr == 5:
        db = DB()
        dataset = search(TEST_SEARCH_PARAMS, db=True)
        db.add_values(dataset[0], dataset[1])
        db.close_conn()
    # run the checker to see data changes
    elif args.test_nr == 6:
        dataset = search(TEST_SEARCH_PARAMS, db=False)
        try:
            checker(data)
        except AssertionError:
            # no changes found
            pass
