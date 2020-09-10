
from inspect import getsourcefile
import os.path
import sys

CUR_PATH = os.path.abspath(getsourcefile(lambda:0))
CUR_DIR = os.path.dirname(CUR_PATH)
PARENT_DIR = CUR_DIR[:CUR_DIR.rfind(os.path.sep)]
sys.path.insert(0, PARENT_DIR)
