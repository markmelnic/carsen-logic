
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from mobile_de.methods import search, checker
from settings import TEST_DATA_FILE, TEST_SEARCH_PARAMS
import scalg, csv

if __name__ == '__main__':
    t = 2
    if t == 1:
        with open(TEST_DATA_FILE, 'r') as csvfile:
            data = list(csv.reader(csvfile))
        dataset = scalg.score_columns(data, [2, 3, 4], [1, 0, 0])
        for dt in dataset:
            print(dt[1:])
    elif t == 2:
        dataset = search(TEST_SEARCH_PARAMS)
        for dt in dataset:
            print(dt[1:])
